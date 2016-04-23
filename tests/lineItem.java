package com.nq.util;
 
import java.io.*;
import java.util.*;
import java.lang.*;
 
class lineItem {
    protected int productId;
    private int ImageID;
    private int qty;
    private int Unitprice;
 
    public lineItem(int prodID, int ImageID, int inQty) {
        productId = prodID;
        this.ImageID = ImageID;
        qty = inQty;
    }
 
    public void setLineItems(Vector lineItems) {
        LineItems = lineItems;
    }
 
    Vector getLineItems() {
        return LineItems;
    }
 
    int getProductID() {
        return productId;
    }
 
    int getImageID() {
        return imageID;
    }
 
    int getQuantity() {
        return qty;
    }
 
    int getUnitPrice() {
        return Unitprice;
    }
 
    public void setProductID(int id) {
        productId = id;
    }
 
    public void setImageID(int ID) {
        imageID = ID;
    }
 
    public void setQty(int qty) {
        this.qty = qty;
    }
 
    public void setUnitPrice(int i) {
        Unitprice = i;
    }
}