const { chromium } = require('playwright')
const fs = require('fs')

function getArgs () {
  const args = process.argv.slice(2)
  const params = {}
  args.forEach((arg) => {
    const [argKey, argValue] = arg.split('=')
    params[argKey] = argValue
  })
  return params
}

function getRangeArr (length) {
  return Array.from({ length }, (_, i) => i + 1)
}

const args = getArgs()
const { match: matchArgument, range } = args
if (!matchArgument) throw new Error('Number of match week must be provided. Example: match=9')

const matchWeekParams = range ? getRangeArr(matchArgument) : [matchArgument]

async function scrap (matchParam) {
  const launchOptions = { headless: false }
  const browser = await chromium.launch(launchOptions)
  const page = await browser.newPage()
  const SCORES_URL = 'https://www.comuniazo.com/comunio-apuestas/puntos'
  const url = `${SCORES_URL}?jornada=${matchParam}`
  await page.goto(url)
  await page.locator('text=ACEPTO')?.click()
  await page.locator('text=Soy mayor de edad')?.click()

  const matches = await page.$$eval('.box-match', (allItems) => {
    const data = {}

    const homeTeamPath = 'a > h2 > div.home'
    const awayTeamPath = 'a > h2 > div.away'

    const homeDomPath = 'ul:first-of-type'
    const awayDomPath = 'ul:last-of-type'

    const playerDomPath = 'li > a'
    const nameDomPath = 'div.row > div.cell > strong'
    const scoreDomPath = 'div.right > div.row > div.cell > span'
    const positionDomPath = 'span'

    const getTeamName = (match, team) => {
      const namePath = team === 'home' ? homeTeamPath : awayTeamPath
      return match.querySelector(namePath).innerText
    }

    const attributes = {
      name: nameDomPath,
      score: scoreDomPath,
      position: positionDomPath
    }

    const positions = {
      'pos-1': 'Goalkeeper',
      'pos-2': 'Defender',
      'pos-3': 'Midfielder',
      'pos-4': 'Forward'
    }

    const getPlayersNodeList = (iterator, team, attribute) => {
      const teamDomPath = team === 'home' ? homeDomPath : awayDomPath
      const attributeDomPath = attributes[attribute]
      const queryStr = [teamDomPath, playerDomPath, attributeDomPath].join(
        ' > '
      )
      return iterator.querySelectorAll(queryStr)
    }

    const getScoreFloat = (str) => {
      const newStr = str.replace(',', '.')
      return parseFloat(newStr)
    }

    allItems.forEach((match) => {
      const homeTeamName = getTeamName(match, 'home')
      const awayTeamName = getTeamName(match, 'away')

      const homePlayerNamesNodeList = getPlayersNodeList(match, 'home', 'name')
      const awayPlayerNamesNodeList = getPlayersNodeList(match, 'away', 'name')

      const homePlayerScoresNodeList = getPlayersNodeList(
        match,
        'home',
        'score'
      )
      const awayPlayerScoresNodeList = getPlayersNodeList(
        match,
        'away',
        'score'
      )

      const homePlayerPositionsNodeList = getPlayersNodeList(
        match,
        'home',
        'position'
      )
      const awayPlayerPositionsNodeList = getPlayersNodeList(
        match,
        'away',
        'position'
      )

      const homePlayerNames = [...homePlayerNamesNodeList].map(
        (playerNode) => playerNode.innerHTML
      )
      const awayPlayerNames = [...awayPlayerNamesNodeList].map(
        (playerNode) => playerNode.innerHTML
      )

      const homePlayerScores = [...homePlayerScoresNodeList].map((playerNode) =>
        getScoreFloat(playerNode.innerHTML)
      )
      const awayPlayerScores = [...awayPlayerScoresNodeList].map((playerNode) =>
        getScoreFloat(playerNode.innerHTML)
      )

      const homePlayerPositions = [...homePlayerPositionsNodeList].map(
        (playerNode) => {
          const positionClassName = playerNode.className.split(' ')[1]
          const position = positions[positionClassName]
          return position
        }
      )

      const awayPlayerPositions = [...awayPlayerPositionsNodeList].map(
        (playerNode) => {
          const positionClassName = playerNode.className.split(' ')[1]
          const position = positions[positionClassName]
          return position
        }
      )

      const homeLineupNum = homePlayerNames.length
      const awayLineupNum = awayPlayerNames.length

      const largestLineup = Math.max(homeLineupNum, awayLineupNum)

      const homePlayers = {}
      const awayPlayers = {}

      for (let i = 0; i < largestLineup; i++) {
        if (i < homeLineupNum) {
          const score = homePlayerScores[i]
          const position = homePlayerPositions[i]
          homePlayers[homePlayerNames[i]] = { position, score }
        }
        if (i < awayLineupNum) {
          const score = awayPlayerScores[i]
          const position = awayPlayerPositions[i]
          awayPlayers[awayPlayerNames[i]] = { position, score }
        }
      }

      const matchKey = `${homeTeamName} - ${awayTeamName}`.trim()
      data[matchKey] = { homePlayers, awayPlayers }
    })
    return data
  })
  const path = `/Users/David/Code/cs50/comunio-clone/integrator/scores/matches/scoresMatch${matchParam}.json`
  const data = JSON.stringify(matches)
  const callback = (err) => {
    if (err) return console.log(err)
    console.log(`Match week ${matchParam} saved in json!`)
  }
  fs.writeFile(path, data, callback)
  await browser.close()
}

const scrapOneByOne = async (matchWeekParams) => {
  for (const matchWeek of matchWeekParams) {
    await scrap(matchWeek)
  }
}

scrapOneByOne(matchWeekParams)
