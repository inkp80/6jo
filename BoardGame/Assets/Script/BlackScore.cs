using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BlackScore : MonoBehaviour {
	private Text blackPiece;

	void Start () {
		blackPiece = GetComponent<Text> ();
	}

	void Update () {
		blackPiece.text = BoardManager.blackPieces.ToString ();
	}
}
