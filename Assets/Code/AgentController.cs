// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class AgentData
{
    //Clase principal de los agentes, la cual guarda el id y la posicion de los agentes
    //creados en el modelo
    public string id;
    public float x, y, z;

    public AgentData(string id, float x, float y, float z)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

[Serializable]
public class CarData : AgentData
{
    //Clase del Agente Coche, que hereda de la clase principal y crea el booleano que indica
    //si el robot tiene una caja en sus manos
    public bool isInDestiny;

    public CarData(string id, float x, float y, float z, bool isInDestiny) : base(id, x, y, z)
    {
        this.isInDestiny = isInDestiny;
    }
}

[Serializable]
public class SemaforoData : AgentData
{
    //Clase del Agente caja, que hereda de la clase principal y crea el booleano que indica
    //si la caja ya fue recogida o no
    public bool state;

    public SemaforoData(string id, float x, float y, float z, bool state) : base(id, x, y, z)
    {
        this.state = state;
    }
}

[Serializable]

public class CarsData
{
    //Clase que permite guardar las posiciones de los agentes Coche, asi como tambien actualizarlas
    public List<CarData> positions;

    public CarsData() => this.positions = new List<CarData>();
}

[Serializable]

public class SemaforosData
{
    //Clase que permite guardar las posiciones de los agentes Caja, asi como tambien actualizarlas
    public List<SemaforoData> positions;

    public SemaforosData() => this.positions = new List<SemaforoData>();
}

[Serializable]

public class AgentsData
{
    public List<AgentData> positions;

    public AgentsData() => this.positions = new List<AgentData>();
}

public class AgentController : MonoBehaviour
{
    // private string url = "https://agents.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getCarsEndpoint = "/getCar";
    string getTrafficEndpoint = "/getTraffic_Light";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    AgentsData agentsData;
    CarsData carsData;
    SemaforosData semaforosData;
    Dictionary<string, GameObject> agents, semaforosVerde;
    Dictionary<string, Vector3> prevPositions, currPositions;

    bool updated = false, started = false, startedLight= false;

    public GameObject coche1Prefab, coche2Prefab, semaforoVerdePrefab, semaforoRojoPrefab;
    public int NCoches;
    public float timeToUpdate = 5.0f;
    private float timer, dt;

    void Start()
    {
        agentsData = new AgentsData();
        carsData = new CarsData();
        semaforosData = new SemaforosData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        semaforosVerde = new Dictionary<string, GameObject>();
        agents = new Dictionary<string, GameObject>();

        // floor.transform.localScale = new Vector3((float)width/10, 1, (float)height/10);
        // floor.transform.localPosition = new Vector3((float)width/2-0.5f, 0, (float)height/2-0.5f);
        
        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());
    }

    private void Update() 
    {
        if(timer < 0)
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach(var agent in currPositions)
            {
                Vector3 currentPosition = agent.Value;
                Vector3 previousPosition = prevPositions[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                 if(semaforosVerde[agent.Key].activeInHierarchy) {
                    semaforosVerde[agent.Key].transform.localPosition = interpolated;
                    if(direction != Vector3.zero) semaforosVerde[agent.Key].transform.rotation = Quaternion.LookRotation(direction);
                }
            }

            // float t = (timer / timeToUpdate);
            // dt = t * t * ( 3f - 2f*t);
        }
    }
 
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetCarsData());
            StartCoroutine(GetSemaforosData());
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NCars", NCoches.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetCarsData());
            StartCoroutine(GetSemaforosData());
        }
    }

    IEnumerator GetCarsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCarsEndpoint); //Modificar EndPoint
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            carsData = JsonUtility.FromJson<CarsData>(www.downloadHandler.text);

            foreach(CarData car in carsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(car.x, car.y, car.z);
                Debug.Log(car.id);

                    if(!started)
                    {
                        prevPositions[car.id] = newAgentPosition;
                            int num = UnityEngine.Random.Range(1, 3);
                            // int num = rnd.Next(1, 3);
                            if (num == 1) {
                                agents[car.id] = Instantiate(coche1Prefab, newAgentPosition, Quaternion.identity);
                            } else {
                                agents[car.id] = Instantiate(coche2Prefab, newAgentPosition, Quaternion.identity);
                            }
                    }
                    else
                    {
                        Vector3 currentPosition = new Vector3();
                        if(currPositions.TryGetValue(car.id, out currentPosition))
                            prevPositions[car.id] = currentPosition;
                        currPositions[car.id] = newAgentPosition;
                        if(car.isInDestiny)
                        {   
                            agents[car.id].SetActive(false);
                        }
                    }
            }

            updated = true;
            if(!started) started = true;
        }
    }

    IEnumerator GetSemaforosData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTrafficEndpoint); //Modificar EndPoint
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            semaforosData = JsonUtility.FromJson<SemaforosData>(www.downloadHandler.text);

            Debug.Log(semaforosData.positions);

            foreach(SemaforoData semaforo in semaforosData.positions)
            {
                if (!startedLight){
                    agents[semaforo.id] = Instantiate(semaforoRojoPrefab, new Vector3(semaforo.x, semaforo.y, semaforo.z), Quaternion.identity);
                    semaforosVerde[semaforo.id] = Instantiate(semaforoVerdePrefab, new Vector3(semaforo.x, semaforo.y, semaforo.z), Quaternion.identity);
                    semaforosVerde[semaforo.id].SetActive(false);
                }
                else{
                    if (semaforo.state) {
                        semaforosVerde[semaforo.id].SetActive(true);
                        agents[semaforo.id].SetActive(false);
                    }
                }
            }
            if (!startedLight) startedLight = true;
        }
    }
}
