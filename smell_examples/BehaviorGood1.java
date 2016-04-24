public class BehaviorGood1 {
  protected String _tagName;

  public HtmlTag( String tagName ) {
    _tagName = tagName;
  }

  public String toString() {
    return ( "<" + _tagName + " " );
  }
}
public class Form extends HtmlTag {
   public Form() {
     super( "form" );
   }
}
public class Table extends HtmlTag {
   public Table() {
     super( "table" );
   }
}