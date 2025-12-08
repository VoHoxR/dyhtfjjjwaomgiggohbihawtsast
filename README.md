**KDN Hoodini**

# Weather App
## City search and display
- Enter a city into the entry box.
  - Weird with how you search, needs to be formatted as A, B
  - A is the city
  - B is either a state, district, country, etc.

### Favorites selector
- dropdown menu just above the entry box
- by default there arent any favorites. To add one:
  1. Enter a city into the search box and press search (or hit enter)
  2. click the 'add to favorites' button at the bottom
  3. when done, the city will appear inside the dropdown when you click it again
- Favorited cities will automatically search when you click on them in the dropdown.
- You can also remove a favorited location. Follow the steps above, but click the 'remove from favorites' button instead. it wont appear in the dropdown anymore until you add it back!

### Unit switching
- When you search for a city, its info will appear in the box below. by default, temperatures are displayed as Celcius. You can change the unit, however, by pressing the 'swap F/C' button at the bottom, which will switch between Fahrenheit and Celcius. the current unit is also displayed at the bottom right.

### Forecast types
- There are two types of forecasts to display:
  1. curent day cast
  2. multi-day cast
- current day is on by default. If you press the '-1/+1 day forecast' buttons under the weather box, You can swap between a 2 day, 3 day, 4 day, and 5 day forecast!
- if you try to cycle up on a 5 day or down on a current day, it will loop around to the other side!

## Implementation
- Implementing everything wasn't too hard. The hardest thing was probably commenting, because most errors in the code were just me being stupid and putting the wrong operator or mispelling something.
### Temperature toggle
- The temp tongle was very easy to add. All i had to do was make a variable to show what unit is being used, and a function to swap it between Fahrenheit and Celcius. By default the API uses Fahrenheit, so I just use the conversion formula to change it to Celcius. ((Temperature - 32) x 5/9)
