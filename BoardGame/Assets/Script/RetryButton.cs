using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class RetryButton : MonoBehaviour {
	private string sceneName = "Game";

	public void RetryGame(){
		UIController.result = false;
		BoardManager.whitePieces = 2;
		BoardManager.blackPieces = 2;
		SceneManager.LoadScene (sceneName);
	}
}
