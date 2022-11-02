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

  const points = await page.$$eval('.player-list-points', (allItems) => {
    const data = []

    const homeDomPath = 'ul:first-of-type'
    const awayDomPath = 'ul:last-of-type'

    const playerDomPath = 'li > a'
    const nameDomPath = 'div.row > div.cell > strong'
    const scoreDomPath = 'div.right > div.row > div.cell > span'

    const getPlayersNodeList = (iterator, team) => {
      const teamDomPath = team === 'home' ? homeDomPath : awayDomPath
      const queryStr = [teamDomPath, playerDomPath, nameDomPath].join(' > ')
      console.log(queryStr)
      return iterator.querySelectorAll(queryStr)
    }

    allItems.forEach((player) => {
      const homePlayersNodeList = getPlayersNodeList(player, 'home')
      const awayPlayersNodeList = getPlayersNodeList(player, 'away')

      const homePlayers = [...homePlayersNodeList].map(
        (playerNode) => playerNode.innerHTML
      )
      const awayPlayers = [...awayPlayersNodeList].map(
        (playerNode) => playerNode.innerHTML
      )

      data.push({ homePlayers, awayPlayers })
    })
    return data
  })
  console.log('points', points)

  await page.locator('.boxes-matches').click()
  await page.screenshot({ path: 'puntuaciones.png' })
  await browser.close()
})()
