using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIManager : MonoBehaviour
{
    [SerializeField] Slider timer;
    [SerializeField] Text score;
    [SerializeField] Text combo;
    [SerializeField] Text hs;
    int lastScore = 0;
    int lastCombo = 0;

    // Start is called before the first frame update
    void Start()
    {
        hs.text = $"BEST: {SwipeManager.instance.highScore}";
    }

    // Update is called once per frame
    void Update()
    {
        if (SwipeManager.instance.score >= 1) hs.enabled = false;
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

        if (SwipeManager.instance.combo >= 2) {
            combo.enabled = true;
            combo.text = "x" + SwipeManager.instance.combo.ToString();
            combo.transform.localScale = Vector3.Lerp(combo.transform.localScale, Vector3.one, Time.deltaTime * 10);
            if (lastCombo != SwipeManager.instance.combo) {
                lastCombo = SwipeManager.instance.combo;
                combo.transform.localScale = Vector3.one * 1.2f;
            }
        } else {
            combo.enabled = false;
        }
    }
}
