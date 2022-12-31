const { chromium } = require('playwright')

const launchOptions = {
  headless: false
}

;(async () => {
  const browser = await chromium.launch(launchOptions)
  const page = await browser.newPage()
  await page.goto('https://www.comuniazo.com/comunio-apuestas/jugadores')
  await page.locator('text=ACEPTO')?.click()
  await page.locator('text=Soy mayor de edad')?.click()

  const players = await page.$$eval('tr.btn', (allItems) => {
    const data = {}

    const teamKeys = {
      1: 'Athletic',
      2: 'Atlético',
      3: 'Barcelona',
      4: 'Betis',
      5: 'Celta',
      7: 'Espanyol',
      8: 'Getafe',
      11: 'Mallorca',
      12: 'Osasuna',
      13: 'Real Sociedad',
      17: 'Sevilla',
      18: 'Valencia',
      19: 'Villarreal',
      21: 'Valladolid',
      22: 'Almería',
      15: 'Real Madrid',
      70: 'Rayo Vallecano',
      75: 'Elche',
      97: 'Girona',
      105: 'Cádiz'
    }

    const positions = {
      'pos-1': 'Goalkeeper',
      'pos-2': 'Defender',
      'pos-3': 'Midfielder',
      'pos-4': 'Forward'
    }

    allItems.forEach(element => {
      console.log(element)
      const nameTag = element.querySelector('td > a > div.player > strong')
      const name = nameTag.innerHTML

      const positionNode = element.querySelector('td > a > span')
      const positionClassName = positionNode.className.split(' ')[1]
      const position = positions[positionClassName]

      const teamImg = element.querySelector('td > a > img')
      const regEx = /teams\/[0-9]+/
      const teamKey = teamImg.src.match(regEx)[0].split('/')[1]
      const team = teamKeys[teamKey]
      data[name] = { position, team }
    })
    return data
  })
  console.log(JSON.stringify(players))
  // await page.screenshot({ path: 'players.png' })
  await browser.close()
})()
