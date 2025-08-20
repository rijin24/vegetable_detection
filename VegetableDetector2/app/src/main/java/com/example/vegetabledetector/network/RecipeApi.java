package com.example.vegetabledetector.network;

import com.google.gson.JsonObject;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface RecipeApi {
    @GET("recipes")
    Call<JsonObject> getRecipes(@Query("vegetable") String vegetableName);
}
