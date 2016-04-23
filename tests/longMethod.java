//long method example
public Class longMethod {
  public String statement(){
    double totalAmount = 0;
    int frequentRenterPoints = 0;
    String result = "Rental record for "+ getName() + "\n";
    for(Rental each : _rentals){
      double thisAmount = 0;
      switch (each.getMovie().getPriceCode()) {
        case Movie.REGULAR:
          thisAmount += 2;
          if ( each.getDaysRented() > 2)
            thisAmount += (each.getDaysRented() - 2 ) * 1.5;
          break;
        case Movie.NEW_RELEASE:
          thisAmount += each.getDaysRented() *3;
          break;
        case Movie.CHILDREN:
          thisAmount += 1.5;
          if (each.getDaysRented() > 3 )
            thisAmount += (each.getDaysRented() - 3)* 1.5;
          break;
      }
      frequentRenterPoints++;
      if ( (each.getMovie().getPriceCode() == Movie.NEW_RELEASE)
            && each.getDaysRented() > 1 )
        frequentRenterPoints ++;
      result += "\t" + each.getMovie().getTitle() + "\t" +
          String.valueOf(thisAmount) + "\n";
      totalAmount += thisAmount;
    }
    result += "Amount owed is "+ String.valueOf(totalAmount)+"\n";
    result += "You earned " + String.valueOf(frequentRenterPoints) +
        " frequent renter points";
    return result;
  }
}