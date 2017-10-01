using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class RestartGame : MonoBehaviour {
	public string sceneName = "Game";

	public void LoadGame(){
		UIController.result = false;
		BoardManager.blackPieces = 2;
		BoardManager.whitePieces = 2;
		SceneManager.LoadScene (sceneName);
	}
}
