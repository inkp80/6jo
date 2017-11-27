using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class WhiteScore : MonoBehaviour {
	private Text whitePiece;

	void Start () {
		whitePiece = GetComponent<Text> ();
	}

	void Update () {
		whitePiece.text = BoardManager.whitePieces.ToString ();
	}
}

