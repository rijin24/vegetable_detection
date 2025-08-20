package com.example.vegetabledetector.ui.recipes;

import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.bumptech.glide.Glide;
import com.example.vegetabledetector.Constants;
import com.example.vegetabledetector.R;

import org.json.JSONArray;
import org.json.JSONObject;

public class RecipeDetailActivity extends AppCompatActivity {

    private TextView tvRecipeName, tvDescription;
    private ImageView recipeImage;
    private LinearLayout ingredientsContainer;
    private String imageUrl, recipeUrl, recipeName;
    String recipesUrl = Constants.BASE_URL ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recipe_detail);

        tvRecipeName = findViewById(R.id.tvRecipeName);
        recipeImage = findViewById(R.id.recipeImage);
        tvDescription = findViewById(R.id.tvDescription);
        ingredientsContainer = findViewById(R.id.ingredientsContainer);

        Intent intent = getIntent();
        recipeName = intent.getStringExtra("name");;
        String description = intent.getStringExtra("description");
        imageUrl = intent.getStringExtra("imageUrl");
        recipeUrl = intent.getStringExtra("recipeUrl");

        tvRecipeName.setText(recipeName);
        tvDescription.setText(description);

        // Load recipe image
        Glide.with(this)
                .load(imageUrl)
                .placeholder(R.drawable.placeholder)
                .into(recipeImage);

        // Open recipe URL on image click
        recipeImage.setOnClickListener(v -> {
            if (recipeUrl != null && !recipeUrl.isEmpty()) {
                Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(recipeUrl));
                startActivity(browserIntent);
            }
        });

        // Load parsed ingredients from API
        fetchIngredientsFromApi(recipeName);
    }

    private void fetchIngredientsFromApi(String recipeName) {
        String url = recipesUrl+"get_ingredients?recipe_name=" + Uri.encode(recipeName);
        RequestQueue queue = Volley.newRequestQueue(this);

        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    JSONArray ingredients = response.optJSONArray("ingredients");
                    if (ingredients != null && ingredients.length() > 0) {
                        for (int i = 0; i < ingredients.length(); i++) {
                            String ingredient = ingredients.optString(i);
                            if (!ingredient.isEmpty()) {
                                addIngredientView(ingredient);
                            }
                        }
                    } else {
                        Toast.makeText(this, "No ingredients found", Toast.LENGTH_SHORT).show();
                    }
                },
                error -> Toast.makeText(this, "Error loading ingredients", Toast.LENGTH_SHORT).show()
        );

        queue.add(request);
    }

    private void addIngredientView(String ingredient) {
        TextView textView = new TextView(this);
        textView.setText("- " + ingredient);
        textView.setTextSize(16);
        textView.setPadding(8, 8, 8, 8);
        textView.setTextColor(Color.BLUE);
        textView.setOnClickListener(v -> checkAvailability(ingredient));
        ingredientsContainer.addView(textView);
    }

    private void checkAvailability(String ingredient) {
        String url = recipesUrl+"vegetable_availability?name=" + Uri.encode(ingredient);
        RequestQueue queue = Volley.newRequestQueue(this);

        JsonObjectRequest jsonRequest = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    // IMPORTANT: Use "available_stores" key according to your API response example
                    JSONArray stores = response.optJSONArray("available_stores");
                    if (stores != null && stores.length() > 0) {
                        StringBuilder message = new StringBuilder("✅ Available at:\n\n");
                        for (int i = 0; i < stores.length(); i++) {
                            JSONObject store = stores.optJSONObject(i);
                            message.append("Store: ").append(store.optString("store_name")).append("\n")
                                    .append("Postcode: ").append(store.optString("postcode")).append("\n")
                                    .append("Stock: ").append(store.optInt("stock")).append("\n\n");
                        }
                        showWarningDialog("Ingredient Available", message.toString(), false);
                    } else {
                        showWarningDialog("⚠️ Not Available", "This ingredient is not available in any nearby stores.", true);
                    }
                },
                error -> Toast.makeText(this, "Error checking availability", Toast.LENGTH_SHORT).show()
        );

        queue.add(jsonRequest);
    }

    private void showWarningDialog(String title, String message, boolean isWarning) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle(title)
                .setMessage(message)
                .setPositiveButton("OK", null);

        AlertDialog dialog = builder.create();

        if (isWarning) {
            dialog.setOnShowListener(d -> dialog.getButton(AlertDialog.BUTTON_POSITIVE).setTextColor(Color.RED));
        }

        dialog.show();
    }
}
