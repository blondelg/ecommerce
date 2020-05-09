# Oscar forked apps
Here is where customising happends. The following Oscar apps have been modified to fit project requirements.
## Analytics
Modify model, add a table to record every article view weather the user is registered to the marketplace or not.
## Order
The first main challenge is to turn Oscar's standard model, which is centralized, into a decentralized model allowing each partner to manage its catalogue and orders on his own. 
Updates on Product model:
* Introduce the concept of order structure, like products, orders structure can be standalone, parent or child. A standalone order is placed upon a single partner whereas a parent order is placed upon different partners. Each partner has his own child order.
* Add a parent field to link parent orders to child orders
The order creator workflow has been modified aswell, for multi partner orders, the parent order is the one seen by the client, when it is submitted, children orders are automatically created and assignated to the corresponding partner. Basket lines are not duplicated, each child order has access to parents lines for its partner.
## Basket
Adding a set of methods on Basket and Line model to manage multi partner baskets. These methods allow to calculate baskets totals ethier for parent but also for child orders, keeping regular behavior untouched for standalone orders.
## Catalogue
Setup a signal-receiver mecanism that sends signals each time a product is seen, creating a record in Analytics ProductView model
* Add a partner field, each product is now directly linked to a partner
* Add a method that calculate the stock level
## Checkout
* Update total order calculator to manage parent-child order structures
## Dashboard
### Catalogue
Add useful fields, remove useless fields
### Order
Setup per partner view
### Report
Add datavizualisation 
## Partner
Only allow Incl tax prices on stock, ext tax prices are calculated automatically.

## Partner
