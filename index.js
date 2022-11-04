const { chromium } = require('playwright')

const launchOptions = {
  headless: false
}

;(async () => {
  const browser = await chromium.launch(launchOptions)
  const page = await browser.newPage()
  await page.goto('https://www.comuniazo.com/comunio-apuestas/puntos')
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

    const getTeamName = (match, team) => {
      const namePath = team === 'home' ? homeTeamPath : awayTeamPath
      return match.querySelector(namePath).innerText
    }

    const getPlayersNodeList = (iterator, team, attribute) => {
      const teamDomPath = team === 'home' ? homeDomPath : awayDomPath
      const attributeDomPath = attribute === 'name' ? nameDomPath : scoreDomPath
      const queryStr = [teamDomPath, playerDomPath, attributeDomPath].join(
        ' > '
      )
      console.log(queryStr)
      return iterator.querySelectorAll(queryStr)
    }

    allItems.forEach((match) => {
      const homeTeamName = getTeamName(match, 'home')
      const awayTeamName = getTeamName(match, 'away')

      const homePlayerNamesNodeList = getPlayersNodeList(match, 'home', 'name')
      const awayPlayerNamesNodeList = getPlayersNodeList(match, 'away', 'name')

      const homePlayerScoresNodeList = getPlayersNodeList(match, 'home', 'score')
      const awayPlayerScoresNodeList = getPlayersNodeList(match, 'away', 'score')

      const homePlayerNames = [...homePlayerNamesNodeList].map(
        (playerNode) => playerNode.innerHTML
      )
      const awayPlayerNames = [...awayPlayerNamesNodeList].map(
        (playerNode) => playerNode.innerHTML
      )

      const homePlayerScores = [...homePlayerScoresNodeList].map(
        (playerNode) => playerNode.innerHTML
      )
      const awayPlayerScores = [...awayPlayerScoresNodeList].map(
        (playerNode) => playerNode.innerHTML
      )

      const homeLineupNum = homePlayerNames.length
      const awayLineupNum = awayPlayerNames.length

      const largestLineup = Math.max(homeLineupNum, awayLineupNum)

      const homePlayers = {}
      const awayPlayers = {}

      for (let i = 0; i < largestLineup; i++) {
        if (i < homeLineupNum) {
          homePlayers[homePlayerNames[i]] = homePlayerScores[i]
        }
        if (i < awayLineupNum) {
          awayPlayers[awayPlayerNames[i]] = awayPlayerScores[i]
        }
      }

      const matchKey = `${homeTeamName} - ${awayTeamName}`.trim()
      data[matchKey] = { homePlayers, awayPlayers }
    })
    return data
  })
  console.log('matches', JSON.stringify(matches))
  // await page.locator('.boxes-matches').click()
  await page.screenshot({ path: 'puntuaciones.png' })
  await browser.close()
})()
