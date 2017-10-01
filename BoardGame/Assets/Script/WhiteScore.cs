using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class WhiteScore : MonoBehaviour {

	private Text text;

	void Start () {
		text = GetComponent<Text> ();
	}

	void Update () {
		text.text = "whitePieces : " + BoardManager.whitePieces.ToString ();
	}
}

