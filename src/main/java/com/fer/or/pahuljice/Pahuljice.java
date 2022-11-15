package com.fer.or.pahuljice;

public class Pahuljice {
    private String cerealName;
    private String type;
    private int numberOfCalories;
    private float price;
    private String storeName;
    private String storeCountryIso;
    private String manufacturerName;
    private String manufacturerCountryIso;
    private String ingredientName;
    private boolean isVegan;
    private boolean isGlutenFree;
    private boolean isAllergenFree;

    public String getCerealName() {
        return cerealName;
    }

    public void setCerealName(String cerealName) {
        this.cerealName = cerealName;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public int getNumberOfCalories() {
        return numberOfCalories;
    }

    public void setNumberOfCalories(int numberOfCalories) {
        this.numberOfCalories = numberOfCalories;
    }

    public float getPrice() {
        return price;
    }

    public void setPrice(float price) {
        this.price = price;
    }

    public String getStoreName() {
        return storeName;
    }

    public void setStoreName(String storeName) {
        this.storeName = storeName;
    }

    public String getStoreCountryIso() {
        return storeCountryIso;
    }

    public void setStoreCountryIso(String storeCountryIso) {
        this.storeCountryIso = storeCountryIso;
    }

    public String getManufacturerName() {
        return manufacturerName;
    }

    public void setManufacturerName(String manufacturerName) {
        this.manufacturerName = manufacturerName;
    }

    public String getManufacturerCountryIso() {
        return manufacturerCountryIso;
    }

    public void setManufacturerCountryIso(String manufacturerCountryIso) {
        this.manufacturerCountryIso = manufacturerCountryIso;
    }

    public String getIngredientName() {
        return ingredientName;
    }

    public void setIngredientName(String ingredientName) {
        this.ingredientName = ingredientName;
    }

    public boolean isVegan() {
        return isVegan;
    }

    public void setVegan(boolean vegan) {
        isVegan = vegan;
    }

    public boolean isGlutenFree() {
        return isGlutenFree;
    }

    public void setGlutenFree(boolean glutenFree) {
        isGlutenFree = glutenFree;
    }

    public boolean isAllergenFree() {
        return isAllergenFree;
    }

    public void setAllergenFree(boolean allergenFree) {
        isAllergenFree = allergenFree;
    }
}
