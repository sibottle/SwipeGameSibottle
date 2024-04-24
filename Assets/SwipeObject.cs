using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SwipeObject : MonoBehaviour
{
    enum Directions{
        Left,Right,Up,Down
    };

    Vector2[] vectorDirections = new Vector2[]{Vector2.left,Vector2.right,Vector2.up,Vector2.down};
    Vector2[] vectorDirectionsAbs = new Vector2[]{Vector2.right,Vector2.right,Vector2.up,Vector2.up};

    [SerializeField] Directions direction;

    [SerializeField] float initScale = 10;
    [SerializeField] float scale = 10;
    [SerializeField] bool touched = false;
    [SerializeField] SpriteRenderer spriteRenderer = null;
    [SerializeField] Sprite[] sprites= new Sprite[4];
    [SerializeField] AudioSource audioSource;
    Touch touch;
    Vector2 sizeCompare;
    Vector3 position = Vector3.zero;
    bool awake = false;
    bool done = false;

    void Start() {
        sizeCompare = new Vector2(Screen.width,Screen.height);
        direction = (Directions)Random.Range(0,4);
        spriteRenderer.sprite = sprites[(int)direction];
        scale = (transform.GetSiblingIndex() + 1)/4f;
        spriteRenderer.color = new Color(1,1,1,0.8f - (transform.GetSiblingIndex() + 1)/4f);
        transform.position = position + Vector3.up*(transform.GetSiblingIndex() + 1) * 2;
    }

    void Setup() {
        awake = true;
        spriteRenderer.sortingOrder = 1;
    }

    void Update()
    {
        transform.localScale = Vector3.one * scale;
        if (done) {
            transform.SetParent(null);
            transform.position += (Vector3)vectorDirections[(int)direction] * Time.deltaTime * 20;
            spriteRenderer.color -= new Color(0,0,0,Time.deltaTime * 10);
            if (!spriteRenderer.isVisible)
                Destroy(gameObject);
            return;
        }
        if (awake) {
            if (Input.touchCount > 0) {
                touch = Input.GetTouch(0);
                if (touch.phase == TouchPhase.Began) {
                    AudioScript.instance.PlaySound(transform.position,0,Random.Range(0.8f,1.2f));
                    Vector2 pos = touch.position / 5;
                    scale = initScale + initScale/5f;
                    Debug.Log(pos);
                    touched = pos.magnitude < 800;
                }
                if (!audioSource.isPlaying) audioSource.Play();
            } else {
                touched = false;
            }
            if (touched) {
                spriteRenderer.color = Color.Lerp(spriteRenderer.color,new Color(1,1,1,0.6f),Time.deltaTime*20);
                scale = Mathf.Lerp(scale,initScale + initScale/8f,Time.deltaTime*20);
                position += (Vector3)(touch.deltaPosition / 200);
                transform.position = Vector3.Lerp(position,position * vectorDirectionsAbs[(int)direction],0.8f);
                audioSource.volume = Mathf.Lerp(audioSource.volume,touch.deltaPosition.magnitude / 10,Time.deltaTime * 70);
                audioSource.pitch = Mathf.Lerp(audioSource.pitch, 1 + touch.deltaPosition.magnitude / 150,Time.deltaTime * 100);
                if (touch.phase == TouchPhase.Ended) {
                    Vector2 mr = transform.position * vectorDirections[(int)direction];
                    float mrRa = mr.x + mr.y;
                    if (Vector3.Distance(position.normalized,vectorDirections[(int)direction]) < 0.8f && transform.position.magnitude >= 1f) {
                        done = true;
                        SwipeManager.instance.SpawnNew();
                        AudioScript.instance.PlaySound(transform.position,2,Random.Range(0.7f,1.3f));
                    } else {
                        SwipeManager.instance.Miss();
                    }
                }
            } else {
                audioSource.volume = Mathf.Lerp(audioSource.volume,0,Time.deltaTime * 20);
                position = Vector3.zero;
                transform.position = Vector3.Lerp(transform.position, position, Time.deltaTime*20);
                scale = Mathf.Lerp(scale,initScale,Time.deltaTime*20);
                spriteRenderer.color = Color.Lerp(spriteRenderer.color,Color.white,Time.deltaTime*20);
            }
        } else {
            scale = Mathf.Lerp(scale,initScale - transform.GetSiblingIndex()/2f,Time.deltaTime*20);
            spriteRenderer.color = Color.Lerp(spriteRenderer.color,new Color(1,1,1,0.8f - transform.GetSiblingIndex()/4f),Time.deltaTime*20);
            transform.position = Vector3.Lerp(transform.position, position + Vector3.up*transform.GetSiblingIndex() * 2, Time.deltaTime*20);
            if (transform.GetSiblingIndex() == 0) Setup();
        }
    }
}
