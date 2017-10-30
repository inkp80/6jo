using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GetAPI : MonoBehaviour {

	public Text plainText;

	public Button button;
	// Use this for initialization
	void Start () {
		plainText.text = "hello";
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	public void requestGetApi(){
		plainText.text = "req GET";
	}


}
