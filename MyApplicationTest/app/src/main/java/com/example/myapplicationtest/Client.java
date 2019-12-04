package com.example.myapplicationtest;// Cal afegir aqui package!

import android.os.AsyncTask;
import android.renderscript.ScriptGroup;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;
import java.net.UnknownHostException;

public class Client extends AsyncTask<Void, Void, String> {

    String dstAddress;
    int dstPort;
    String response = "";
    TextView textResponse;

    Client(String addr, int port, TextView textResponse) {
        dstAddress = addr;
        dstPort = port;
        this.textResponse = textResponse;
    }

    @Override
    protected String doInBackground(Void... arg0) {

        Socket socket = null;

        try {
            socket = new Socket(dstAddress, dstPort);

            DataOutputStream out = new DataOutputStream(socket.getOutputStream());
            byte[] buffer = new byte[1024];

            String resp;
            DataInputStream in = new DataInputStream(socket.getInputStream());

            JSONObject json = new JSONObject();
            JSONObject params = new JSONObject();
            params.put("user_id", 1);
            json.put("user_id", 1);
            json.put("function", "CHECK_USER");
            json.put("parameters", params);

            String query = json.toString();
            out.writeUTF(query);

            /*
             * notice: inputStream.read() will block if no data return
             */
            in.read(buffer);
            resp = new String(buffer, "UTF-8");
            System.out.println(resp);
            while (!resp.contains("end")) {
                out.writeUTF("Exit");
                response += resp;
                in.read(buffer);
                resp = new String(buffer, "UTF-8");
            }

        } catch (UnknownHostException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            response = "UnknownHostException: " + e.toString();
        } catch (IOException | JSONException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            response = "IOException: " + e.toString();
        } finally {
            if (socket != null) {
                try {
                    socket.close();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
        }
        return response;
    }

    @Override
    protected void onPostExecute(String result) {
        textResponse.setText(response);
        super.onPostExecute(result);
    }

}