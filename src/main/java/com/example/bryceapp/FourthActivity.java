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
import android.widget.ImageView;




public class FourthActivity extends AppCompatActivity {
    //Developed from CS 496 module http://classes.engr.oregonstate.edu/eecs/winter2017/cs496/module-6/basic-activity.html
    private ArrayList<Integer> gridNumbers = new ArrayList<Integer>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fourth);
    }
}
