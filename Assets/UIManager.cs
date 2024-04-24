using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIManager : MonoBehaviour
{
    [SerializeField] Slider timer;
    [SerializeField] Text score;
    int lastScore = 0;

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        score.transform.localScale = Vector3.Lerp(score.transform.localScale, Vector3.one,Time.deltaTime * 10);
        timer.maxValue = SwipeManager.instance.maxTime;
        timer.value = SwipeManager.instance.nextTime;
        if (lastScore != SwipeManager.instance.score) {
            if (SwipeManager.instance.score == SwipeManager.instance.highScore)
                score.color = new Color(255,240,0);
            score.text = SwipeManager.instance.score.ToString();
            score.transform.localScale = Vector3.one * 1.2f;
            lastScore = SwipeManager.instance.score;
        }
    }
}
