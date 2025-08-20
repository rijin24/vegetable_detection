package com.example.vegetabledetector.ui.detected;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.navigation.Navigation;

import com.example.vegetabledetector.R;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

public class DetectedVegetableFragment extends Fragment {

    private static final String ARG_VEGETABLE_NAME = "vegetable_name";
    private String vegetableName;

    // Factory method to create fragment with vegetable name argument
    public static DetectedVegetableFragment newInstance(String name) {
        DetectedVegetableFragment fragment = new DetectedVegetableFragment();
        Bundle args = new Bundle();
        args.putString(ARG_VEGETABLE_NAME, name);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Retrieve the vegetable name passed in the arguments bundle
        if (getArguments() != null) {
            vegetableName = getArguments().getString(ARG_VEGETABLE_NAME);
        }
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the fragment layout
        View view = inflater.inflate(R.layout.fragment_detected_vegetable, container, false);

        // Get references to UI elements
        TextView vegNameText = view.findViewById(R.id.vegetable_name);
        FloatingActionButton recipeButton = view.findViewById(R.id.view_recipes_button);

        // Set the text dynamically to show detected vegetable name
        vegNameText.setText("Your Veggie Match: " + vegetableName);

        // Set click listener on FAB to navigate to recipes fragment, passing vegetable name
        recipeButton.setOnClickListener(v -> {
            Bundle bundle = new Bundle();
            bundle.putString(ARG_VEGETABLE_NAME, vegetableName);
            Navigation.findNavController(v).navigate(R.id.action_detectedVegetableFragment_to_recipesFragment, bundle);
        });

        return view;
    }
}
