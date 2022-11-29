using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CityMaker : MonoBehaviour
{
     [SerializeField] TextAsset layout;
    [SerializeField] GameObject roadPrefab;
    [SerializeField] GameObject roadPrefab2;
    [SerializeField] GameObject building1Prefab;
    [SerializeField] GameObject building2Prefab;
    [SerializeField] GameObject building3Prefab;
    [SerializeField] GameObject building4Prefab;
    [SerializeField] GameObject destiny1Prefab;
    [SerializeField] GameObject destiny2Prefab;
    [SerializeField] GameObject semaphorePrefab;
    [SerializeField] GameObject grass;
    [SerializeField] int tileSize;
    public List<(int, int)> semaforosArriba;
    public List<(int, int)> semaforosAbajo;
    public List<(int, int)> semaforosDerecha;
    public List<(int, int)> semaforosIzquierda;
    public List<(int, int)> destinosArriba;
    public List<(int, int)> destinosAbajo;
    public List<(int, int)> destinosDerecha;
    public List<(int, int)> destinosIzquierda;

    // Start is called before the first frame update
    void Start()
    {
        semaforosArriba = new List<(int, int)> {(0, 13), (1, 13), (6, 2), (7, 2), (13, 2), (14, 2)};
        semaforosAbajo = new List<(int, int)> {(6, 16), (7, 16), (22, 7), (23, 7), (16, 22), (17, 22)};
        semaforosDerecha = new List<(int, int)> {(2, 12), (2, 11), (8, 18), (8, 17), (18, 23), (18, 24)};
        semaforosIzquierda = new List<(int, int)> {(5, 0), (5, 1), (12, 0), (12, 1), (21, 9), (21, 8)};
        
        destinosArriba = new List<(int, int)> {(3, 22), (10, 7)};
        destinosAbajo = new List<(int, int)> {(3, 19), (19, 2)};
        destinosDerecha = new List<(int, int)> {(5, 4), (12, 4), (21, 5), (21, 22), (12, 20), (12, 15), (5, 15)};
        destinosIzquierda = new List<(int, int)> {(2, 15), (18, 14), (18, 20)};
        MakeTiles(layout.text);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void MakeTiles(string tiles)
    {
        int x = 0;
        // Mesa has y 0 at the bottom
        // To draw from the top, find the rows of the file
        // and move down
        // Remove the last enter, and one more to start at 0
        int y = tiles.Split('\n').Length - 2;
        Debug.Log(y);

        Vector3 position;
        Vector3 positionRoad;
        Vector3 positionSemaf;
        GameObject tile;

        for (int i=0; i<tiles.Length; i++) {
            if (tiles[i] == '>' || tiles[i] == '<') {
                position = new Vector3((x * tileSize) + .4f, 0, (y * tileSize) + .4f);
                tile = Instantiate(roadPrefab2, position, Quaternion.Euler(-90, 0, -90));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'v' || tiles[i] == '^') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(-90, 0, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 's') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                positionRoad = new Vector3((x * tileSize) + .4f, 0, (y * tileSize) + .4f);
                tile = Instantiate(roadPrefab, positionRoad, Quaternion.Euler(-90, 0, -90));
                tile.transform.parent = transform;
                if (semaforosIzquierda.Contains((x, y))) { 
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, -90, 0));
                }
                else if (semaforosDerecha.Contains((x, y))) { 
                    positionSemaf = new Vector3((x * tileSize), 0, (y * tileSize) + .8f);
                    tile = Instantiate(semaphorePrefab, positionSemaf, Quaternion.Euler(0, 90, 0));
                }
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'S') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(-90, 0, 0));
                tile.transform.parent = transform;
                if (semaforosArriba.Contains((x, y))) {
                    positionSemaf = new Vector3((x * tileSize) - .4f, 0, (y * tileSize));
                    tile = Instantiate(semaphorePrefab, positionSemaf, Quaternion.Euler(0, 0, 0));
                }
                else if (semaforosAbajo.Contains((x, y))) {
                    positionSemaf = new Vector3((x * tileSize) + .4f, 0, (y * tileSize)); 
                    tile = Instantiate(semaphorePrefab, positionSemaf, Quaternion.Euler(0, 180, 0));
                }
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'D') {
                position = new Vector3(x * tileSize, 0, (y * tileSize) + .4f);
                tile = Instantiate(grass, position, Quaternion.identity);
                int num = UnityEngine.Random.Range(1, 3);
                    if (num == 1) {
                        position = new Vector3(x * tileSize, 0, (y * tileSize) + .4f);
                        if (destinosArriba.Contains((x, y))) tile = Instantiate(destiny1Prefab, position, Quaternion.Euler(-90, 90, 0));
                        if (destinosAbajo.Contains((x, y))) tile = Instantiate(destiny1Prefab, position, Quaternion.Euler(-90, -90, 0));
                        if (destinosDerecha.Contains((x, y))) tile = Instantiate(destiny1Prefab, position, Quaternion.Euler(-90, 180, 0));
                        if (destinosIzquierda.Contains((x, y))) tile = Instantiate(destiny1Prefab, position, Quaternion.Euler(-90, 0, 0));
                    } else {
                        if (destinosArriba.Contains((x, y))) {
                            position = new Vector3((x * tileSize) + 0.284f, 0, (y * tileSize) + 0.548f);
                            tile = Instantiate(destiny2Prefab, position, Quaternion.Euler(0, 90, 0));
                        } else if (destinosAbajo.Contains((x, y))) {
                          position = new Vector3((x * tileSize) -0.262f, 0, (y * tileSize) + 0.25f);
                          tile = Instantiate(destiny2Prefab, position, Quaternion.Euler(0, -90, 0));
                        } else if (destinosDerecha.Contains((x, y))) {
                            position = new Vector3((x * tileSize) - 0.037f, 0, (y * tileSize) + 0.548f);
                            tile = Instantiate(destiny2Prefab, position, Quaternion.Euler(0, 0, 0));
                        } else if (destinosIzquierda.Contains((x, y))) {
                            position = new Vector3((x * tileSize) + 0.066f, 0, (y * tileSize) + 0.178f);
                            tile = Instantiate(destiny2Prefab, position, Quaternion.Euler(0, 180, 0));
                        }
                        tile.transform.localScale = new Vector3(.055f, .036f, .022f);
                    }
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '#') {
                position = new Vector3(x * tileSize, 0, (y * tileSize) + .4f);
                tile = Instantiate(grass, position, Quaternion.identity);
                int num = UnityEngine.Random.Range(1, 5);
                    if (num == 1) {
                        position = new Vector3(x * tileSize, 0, (y * tileSize) + .4f);
                        tile = Instantiate(building1Prefab, position, Quaternion.identity);
                        tile.transform.localScale = new Vector3(.6f, Random.Range(0.5f, 2.0f), .7f);
                    } else if (num == 2) {
                        position = new Vector3(x * tileSize, -.1f, (y * tileSize) + .4f);
                        tile = Instantiate(building2Prefab, position, Quaternion.Euler(-90, 0, 0));
                        tile.transform.localScale = new Vector3(.075f, .06f, .075f);
                    } else if (num == 3) {
                        position = new Vector3(x * tileSize, -.1f, (y * tileSize) + .4f);
                        tile = Instantiate(building3Prefab, position, Quaternion.Euler(-90, 0, 0));
                        tile.transform.localScale = new Vector3(.075f, .06f, .075f);
                    } else {
                        position = new Vector3(x * tileSize, -.1f, (y * tileSize) + .4f);
                        tile = Instantiate(building4Prefab, position, Quaternion.Euler(0, 0, 0));
                    }
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '\n') {
                x = 0;
                y -= 1;
            }
        }

    }
}
