using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SwipeManager : MonoBehaviour
{
    static public SwipeManager instance;
    [SerializeField] GameObject mainObject;
    [SerializeField] public int score;
    [SerializeField] public float nextTime;
    [SerializeField] public float maxTime;
    [SerializeField] public int highScore = 0;
    [SerializeField] public int combo = 0;
    [SerializeField] public AudioClip tapSound;
    [SerializeField] public AudioClip failSound;
    [SerializeField] public AudioSource audioSource;
    float shake = 0;
 
    void Start()
    {
        instance = this;
        if (PlayerPrefs.HasKey("highScore")) 
            highScore = PlayerPrefs.GetInt("highScore");
    }

    // Update is called once per frame
    void Update()
    {
        if (nextTime > 0) nextTime -= Time.deltaTime;
        else {
            if (score > 0) {
                PlayerPrefs.SetInt("highScore",highScore);
                SceneManager.LoadScene("SampleScene");
            }
        }
        shake = Mathf.MoveTowards(shake, 0, Time.deltaTime);
        Camera.main.transform.eulerAngles = new Vector3(Random.Range(-shake,shake),Random.Range(-shake,shake),Random.Range(-shake,shake));
    }

    public void SpawnNew() {
        score++;
        maxTime = 0.2f + 3f / (1f + score/200f);
        nextTime = maxTime;
        Instantiate(mainObject,transform).transform.SetAsLastSibling();
        if (score > highScore) highScore = score;
        combo++;
    }

    public void Miss() {
        if (combo >= 20) AudioScript.instance.PlaySound(Vector3.zero,3,1,0.8f);
        AudioScript.instance.PlaySound(Vector2.zero,1);
        combo = 0;
        nextTime -= 0.2f;
        shake = 0.3f;
    }
}
