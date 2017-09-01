package com.example.bryceapp;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import java.util.ArrayList;
import android.widget.Button;
import android.widget.GridView;
import android.widget.ArrayAdapter;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.AdapterView;
import android.widget.Toast;
import android.widget.BaseAdapter;
import android.widget.LinearLayout;

public class SecondActivity extends AppCompatActivity {
    private ArrayList<Integer> horizontalNumbers = new ArrayList<Integer>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);
        horizontalNumbers.add(1);
        horizontalNumbers.add(2);
        horizontalNumbers.add(3);
        horizontalNumbers.add(4);
        horizontalNumbers.add(5);
        horizontalNumbers.add(6);

    }
}
