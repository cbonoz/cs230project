public abstract class BehaviorBad1 {
  abstract public String toString();
}
public class Form extends HtmlTag {
  public Form() {
    super();
  }
  public String toString() {
     return ( "<form " );
  }
}
public class Table extends HtmlTag {
  public Table() {
    super();
  }
  public String toString() {
     return ( "<table " );
  }
}


