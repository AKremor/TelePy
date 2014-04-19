package com.ldunn.myapplication.app;

import android.content.Context;
import android.location.Location;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesClient;
import com.google.android.gms.location.LocationClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;

import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Timer;
import java.util.TimerTask;

public class MainActivity extends ActionBarActivity implements
        GooglePlayServicesClient.ConnectionCallbacks,
        GooglePlayServicesClient.OnConnectionFailedListener,
        LocationListener {

    LocationClient mLocationClient;
    Location mLocation;
    LocationRequest mLocationRequest;
    Timer mRequestTimer;
    HttpURLConnection mConnection;
    URL mURL;

    String testPayload = "{lat:-33.86,long:151.211}";
    String mPayload = "http://137.147.85.173:8000/cgi-bin/TelePy/round3.cgi";
    double mEarthRadius = 6371;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mLocationClient = new LocationClient(this,this,this);
        mLocationRequest = LocationRequest.create();
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        mLocationRequest.setInterval(5000);
        mLocationRequest.setFastestInterval(1000);

        mRequestTimer = new Timer();
        final Context ctxt = this;
        mRequestTimer.schedule(new TimerTask() {
            public void run() {
                try {
                    mConnection = (HttpURLConnection) mURL.openConnection();
                    InputStream in = new BufferedInputStream(mConnection.getInputStream());
                    BufferedReader reader = new BufferedReader(new InputStreamReader(in));
                    mPayload = reader.readLine();
                    Toast.makeText(ctxt, mPayload, Toast.LENGTH_SHORT).show();
                }
                catch (Exception e) {
                    Toast.makeText(ctxt,"Fetching coords failed", Toast.LENGTH_SHORT).show();
                }

            }
        }, 15000);

        final EditText editURL = (EditText) findViewById(R.id.serverURL);
        final Context ctxt = this;
        Button btnSetURL = (Button) findViewById(R.id.setURL);
        btnSetURL.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    mURL = new URL(editURL.getText().toString());
                }
                catch (Exception e) {
                    Toast.makeText(ctxt,"Invalid URL", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    @Override
    protected void onStart() {
        super.onStart();
        mLocationClient.connect();
    }

    @Override
    protected void onStop() {
        mLocationClient.disconnect();
        super.onStop();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onConnected(Bundle dataBundle) {
        Toast.makeText(this, "Connected to location services", Toast.LENGTH_SHORT).show();
        mLocationClient.requestLocationUpdates(mLocationRequest, this);
    }

    @Override
    public void onDisconnected() {
        Toast.makeText(this, "Lost connection to location services", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onConnectionFailed(ConnectionResult res) {
        return;
    }

    @Override
    public void onLocationChanged(Location location) {
        mLocation = location;

        double latitude = mLocation.getLatitude();
        double longitude = mLocation.getLongitude();

        float[] results = {0,0,0};
        double testLat, testLong, distance, bearing;

        try {
            JSONObject payload = new JSONObject(testPayload);
            testLat = payload.getDouble("latitude");
            testLong = payload.getDouble("longitude");
            Location.distanceBetween(latitude, longitude, testLat, testLong, results);
            distance = results[0];
            bearing = results[1];
        }
        catch (Exception e) {
            Toast.makeText(this, "Received malformed JSON payload!",Toast.LENGTH_SHORT);
            return;
        }

        TextView textLat = (TextView) findViewById(R.id.phoneLat);
        textLat.setText(String.valueOf(latitude));

        TextView textLong = (TextView) findViewById(R.id.phoneLong);
        textLong.setText(String.valueOf(longitude));

        TextView textDistance = (TextView) findViewById(R.id.distance);
        textDistance.setText(String.valueOf(distance));

        TextView textBearing = (TextView) findViewById(R.id.bearing);
        textBearing.setText(String.valueOf(bearing));
    }
}
