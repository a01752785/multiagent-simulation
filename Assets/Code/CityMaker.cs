using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CityMaker : MonoBehaviour
{
     [SerializeField] TextAsset layout;
    [SerializeField] GameObject roadPrefab;
    [SerializeField] GameObject building1Prefab;
    [SerializeField] GameObject building2Prefab;
    [SerializeField] GameObject destiny1Prefab;
    [SerializeField] GameObject destiny2Prefab;
    [SerializeField] GameObject semaphorePrefab;
    [SerializeField] int tileSize;
    public List<(int, int)> semaforosArriba;
    public List<(int, int)> semaforosAbajo;
    public List<(int, int)> semaforosDerecha;
    public List<(int, int)> semaforosIzquierda;

    // Start is called before the first frame update
    void Start()
    {
        semaforosArriba = new List<(int, int)> {(0, 12), (1, 12), (6, 1), (7, 1), (13, 1), (14, 1)};
        semaforosAbajo = new List<(int, int)> {(6, 15), (7, 15), (22, 6), (23, 6), (16, 21), (17, 21)};
        semaforosDerecha = new List<(int, int)> {(2, 11), (2, 10), (8, 17), (8, 16), (18, 22), (18, 23)};
        semaforosIzquierda = new List<(int, int)> {(5, -1), (5, 0), (12, -1), (12, 0), (21, 8), (21, 7)};
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
        GameObject tile;

        for (int i=0; i<tiles.Length; i++) {
            if (tiles[i] == '>' || tiles[i] == '<') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'v' || tiles[i] == '^') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 's') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                if (semaforosArriba.Contains((x, y))) { 
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 90, 0));
                }
                else if (semaforosAbajo.Contains((x, y))) { 
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, -90, 0));
                }
                else if (semaforosIzquierda.Contains((x, y))) { 
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 180, 0));
                }
                else if (semaforosDerecha.Contains((x, y))) { 
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 0, 0));
                }
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'S') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                
                if (semaforosArriba.Contains((x, y))) {
                    tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                    tile.transform.parent = transform; 
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 90, 0));
                    tile.transform.parent = transform;
                }
                else if (semaforosAbajo.Contains((x, y))) { 
                    tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                    tile.transform.parent = transform;
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, -90, 0));
                    tile.transform.parent = transform;
                }
                else if (semaforosIzquierda.Contains((x, y))) {
                    tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                    tile.transform.parent = transform; 
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 180, 0));
                    tile.transform.parent = transform;
                }
                else if (semaforosDerecha.Contains((x, y))) {
                    tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                    tile.transform.parent = transform; 
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 0, 0));
                    tile.transform.parent = transform;
                }
                x += 1;
            } else if (tiles[i] == 'D') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(building1Prefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '#') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(building1Prefab, position, Quaternion.identity);
                tile.transform.localScale = new Vector3(1, Random.Range(0.5f, 2.0f), 1);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '\n') {
                x = 0;
                y -= 1;
            }
        }

    }
}
