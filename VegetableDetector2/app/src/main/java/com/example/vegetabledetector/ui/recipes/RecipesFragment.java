package com.example.vegetabledetector.ui.recipes;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.android.volley.Request;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.example.vegetabledetector.R;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.util.ArrayList;
import java.util.List;

public class RecipesFragment extends Fragment {
    private static final String ARG_VEGETABLE_NAME = "vegetable_name";
    private RecyclerView recyclerView;
    private RecipeAdapter adapter;
    private TextView tvVegetableName;

    public static RecipesFragment newInstance(String vegetableName) {
        RecipesFragment fragment = new RecipesFragment();
        Bundle args = new Bundle();
        args.putString(ARG_VEGETABLE_NAME, vegetableName);
        fragment.setArguments(args);
        return fragment;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_recipes, container, false);

        tvVegetableName = view.findViewById(R.id.tvVegetableName);
        recyclerView = view.findViewById(R.id.recipesRecyclerView);
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));

        String vegetableName = getArguments() != null ? getArguments().getString(ARG_VEGETABLE_NAME) : "Unknown";
        tvVegetableName.setText(vegetableName);

        fetchRecipesFromAPI(vegetableName);

        return view;
    }

    private void fetchRecipesFromAPI(String vegetableName) {
        String url = "http://172.20.10.3:5000/get_recipes?vegetable=" + vegetableName;

        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    List<Recipe> recipes = new ArrayList<>();
                    try {
                        JSONArray recipeArray = response.getJSONArray("recipes");
                        for (int i = 0; i < recipeArray.length(); i++) {
                            JSONObject obj = recipeArray.getJSONObject(i);
                            recipes.add(new Recipe(
                                    obj.getString("RECIPENAME"),
                                    obj.getString("RECIPEURL"),
                                    obj.getString("DESCRIPTION")
                            ));
                        }
                        adapter = new RecipeAdapter(getContext(), recipes);
                        recyclerView.setAdapter(adapter);
                    } catch (JSONException e) {
                        Toast.makeText(getContext(), "Error parsing recipes", Toast.LENGTH_SHORT).show();
                    }
                },
                error -> Toast.makeText(getContext(), "API error: " + error.getMessage(), Toast.LENGTH_SHORT).show()
        );

        Volley.newRequestQueue(getContext()).add(request);
    }
}
