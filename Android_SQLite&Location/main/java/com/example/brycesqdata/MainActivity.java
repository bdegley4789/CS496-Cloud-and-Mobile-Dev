package com.example.brycesqdata;

import android.os.Bundle;
import android.app.AlertDialog;
import android.database.Cursor;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import android.location.LocationManager;
import android.location.Criteria;
import android.location.Location;
import android.location.LocationListener;
import android.os.Build;
import android.annotation.TargetApi;
import android.widget.TextView;
import java.util.ArrayList;
import android.Manifest;
import android.app.Service;
import android.util.Log;
import android.content.pm.PackageManager;

//For sqlite database I used portions and modified code from open source tutorial here and commented on how code works as the syllabus says
//http://www.codebind.com/android-tutorials-and-examples/android-sqlite-tutorial-example/
//For getting location and permissions in android I used portions and modified code from open source tutorial here and commented on how code works
//http://en.proft.me/2017/04/17/how-get-location-latitude-longitude-gps-android/
public class MainActivity extends ActionBarActivity  implements LocationListener {
    DatabaseHelper myDb;
    EditText editMessage,editLatitude,editLongitude;
    Button btnAddData;
    Button btnviewAll;
    final String TAG = "GPS";
    private final static int ALL_PERMISSIONS_RESULT = 101;
    private static final long MIN_DISTANCE_CHANGE_FOR_UPDATES = 10;
    private static final long MIN_TIME_BW_UPDATES = 1000 * 60 * 1;
    TextView tvLatitude, tvLongitude;
    LocationManager locationManager;
    Location loc;
    ArrayList<String> permissions = new ArrayList<>();
    ArrayList<String> permissionsToRequest;
    ArrayList<String> permissionsRejected = new ArrayList<>();
    boolean isGPS = false;
    boolean isNetwork = false;
    boolean canGetLocation = true;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        myDb = new DatabaseHelper(this);
        //Values for Front end display of my app
        editMessage = (EditText)findViewById(R.id.editText_Message);
        editLatitude = (EditText)findViewById(R.id.editText_Latitude);
        editLongitude = (EditText)findViewById(R.id.editText_Longitude);
        btnAddData = (Button)findViewById(R.id.button_add);
        btnviewAll = (Button)findViewById(R.id.button_viewAll);

        //Main Functions of app
        AddData();
        viewAll();
        //Location values for latitude and longitude
        tvLatitude = (TextView) findViewById(R.id.editText_Latitude);
        tvLongitude = (TextView) findViewById(R.id.editText_Longitude);
        locationManager = (LocationManager) getSystemService(Service.LOCATION_SERVICE);
        isGPS = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER);
        isNetwork = locationManager.isProviderEnabled(LocationManager.NETWORK_PROVIDER);
        permissions.add(Manifest.permission.ACCESS_FINE_LOCATION);
        permissions.add(Manifest.permission.ACCESS_COARSE_LOCATION);
        permissionsToRequest = findUnAskedPermissions(permissions);
        //Check if GPS and Netowrk features are running
        if (!isGPS && !isNetwork) {
            Log.d(TAG, "Connection off");
            getLastLocation();
        } else {
            Log.d(TAG, "Connection on");
            // check that permissions are on for location
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                if (permissionsToRequest.size() > 0) {
                    requestPermissions(permissionsToRequest.toArray(new String[permissionsToRequest.size()]),
                            ALL_PERMISSIONS_RESULT);
                    Log.d(TAG, "Permission requests");
                    canGetLocation = false;
                }
            }
            getLocation();
        }
    }
    //Insert message with current latitude and longitude on front end in SQLite database
    public  void AddData() {
        btnAddData.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        boolean isInserted = myDb.insertData(editMessage.getText().toString(),
                                editLatitude.getText().toString(),
                                editLongitude.getText().toString() );
                        if(isInserted == true)
                            Toast.makeText(MainActivity.this,"Data Inserted",Toast.LENGTH_LONG).show();
                        else
                            Toast.makeText(MainActivity.this,"Data not Inserted",Toast.LENGTH_LONG).show();
                    }
                }
        );
    }
    //View all the data currently in the SQLite Database for your local device
    public void viewAll() {
        btnviewAll.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        Cursor res = myDb.getAllData();
                        if(res.getCount() == 0) {
                            // show message
                            showMessage("Error","Nothing found");
                            return;
                        }
                        StringBuffer buffer = new StringBuffer();
                        //Query data with while loop, move through entire database
                        while (res.moveToNext()) {
                            buffer.append("Id :"+ res.getString(0)+"\n");
                            buffer.append("Message :"+ res.getString(1)+"\n");
                            buffer.append("Latitude :"+ res.getString(2)+"\n");
                            buffer.append("Longitude :"+ res.getString(3)+"\n\n");
                        }
                        // Show all data
                        showMessage("Data",buffer.toString());
                    }
                }
        );
    }
    //Display Database query results to alert dialog
    public void showMessage(String title,String Message){
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setCancelable(true);
        builder.setTitle(title);
        builder.setMessage(Message);
        builder.show();
    }
    //Location methods
    @Override
    public void onLocationChanged(Location location) {
        Log.d(TAG, "onLocationChanged");
        updateUI(location);
    }
    //Overrides the abstract method for location listener
    @Override
    public void onStatusChanged(String s, int i, Bundle bundle) {}
    //Overrides the abstract method for location listener
    @Override
    public void onProviderEnabled(String s) {
        getLocation();
    }
    //Overrides the abstract method for location listener
    @Override
    public void onProviderDisabled(String s) {
        if (locationManager != null) {
            locationManager.removeUpdates(this);
        }
    }
    //Gets current location set on adnroid device. If device is emulator it will display last entered location
    private void getLocation() {
        try {
            //Checks if location is accessible
            if (canGetLocation) {
                Log.d(TAG, "Can get location");
                if (isGPS) {
                    //Goes over GDPs to make sure location managers gives access
                    Log.d(TAG, "GPS on");
                    locationManager.requestLocationUpdates(
                            LocationManager.GPS_PROVIDER,
                            MIN_TIME_BW_UPDATES,
                            MIN_DISTANCE_CHANGE_FOR_UPDATES, this);
                    //Will use last location entered if in emulator
                    if (locationManager != null) {
                        loc = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                        if (loc != null)
                            updateUI(loc);
                    }
                } else if (isNetwork) {
                    //Checks for changes to location, I removed the time feature when modifying the code from the tutorial
                    Log.d(TAG, "NETWORK_PROVIDER on");
                    locationManager.requestLocationUpdates(
                            LocationManager.NETWORK_PROVIDER,
                            MIN_TIME_BW_UPDATES,
                            MIN_DISTANCE_CHANGE_FOR_UPDATES, this);

                    if (locationManager != null) {
                        loc = locationManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
                        if (loc != null)
                            updateUI(loc);
                    }
                } else {
                    //For OSU coordinates
                    loc.setLatitude(44.5);
                    loc.setLongitude(-123.2 );
                    updateUI(loc);
                }
            } else {
                Log.d(TAG, "Can't get location");
            }
        } catch (SecurityException e) {
            e.printStackTrace();
        }
    }
    //Used in onCreate if connection is off this will retrieve the most recent location for the device
    private void getLastLocation() {
        try {
            Criteria criteria = new Criteria();
            String provider = locationManager.getBestProvider(criteria, false);
            Location location = locationManager.getLastKnownLocation(provider);
            Log.d(TAG, provider);
            Log.d(TAG, location == null ? "NO LastLocation" : location.toString());
        } catch (SecurityException e) {
            e.printStackTrace();
        }
    }
    //Get permission for location first time when it's turned off and user hasn't yet given permission
    private ArrayList findUnAskedPermissions(ArrayList<String> wanted) {
        ArrayList result = new ArrayList();

        for (String perm : wanted) {
            if (!hasPermission(perm)) {
                result.add(perm);
            }
        }
        return result;
    }
    //If user already gave permission then permissions continue to turned on
    private boolean hasPermission(String permission) {
        if (canAskPermission()) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                return (checkSelfPermission(permission) == PackageManager.PERMISSION_GRANTED);
            }
        }
        return true;
    }
    //Check if app is allowed to ask device for permission
    private boolean canAskPermission() {
        return (Build.VERSION.SDK_INT > Build.VERSION_CODES.LOLLIPOP_MR1);
    }
    //Get's location if user says yes to permission request if not it will not change location values and just use default values for OSU I gave in the xml for location
    @TargetApi(Build.VERSION_CODES.M)
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        switch (requestCode) {
            case ALL_PERMISSIONS_RESULT:
                Log.d(TAG, "onRequestPermissionsResult");
                for (String perms : permissionsToRequest) {
                    if (!hasPermission(perms)) {
                        permissionsRejected.add(perms);
                    }
                }
                if (permissionsRejected.size() > 0) {
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                        if (shouldShowRequestPermissionRationale(permissionsRejected.get(0))) {
                        }
                    }
                } else {
                    Log.d(TAG, "No rejected permissions.");
                    canGetLocation = true;
                    getLocation();
                }
                break;
        }
    }
    //Updates location to new longitude and latitude passed through loc
    private void updateUI(Location loc) {
        Log.d(TAG, "updateUI");
        tvLatitude.setText(Double.toString(loc.getLatitude()));
        tvLongitude.setText(Double.toString(loc.getLongitude()));
    }
}

