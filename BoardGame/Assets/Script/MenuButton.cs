using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class MenuButton : MonoBehaviour {
	public Light mainLight;
	public Text pauseText;

	public Button resumeButton;
	public Button terminateButton;


	public void MenuOpen() {
		BoardManager.nextFire = Time.time + 1.0f;

		if (BoardManager.pauseFlag) {
			resumeGame ();
		} else {
			stopGame ();
		}
	}

	public void terminateStage(){
		BoardManager.pauseFlag = false;
		SceneManager.LoadScene ("MainUI");
	}

	public void resumeGame(){
		BoardManager.pauseFlag = false;
		mainLight.intensity = 1.0f;
		pauseText.enabled = false;
		resumeButton.gameObject.SetActive (false);
		terminateButton.gameObject.SetActive (false);
	}

	public void stopGame(){
		BoardManager.pauseFlag = true;
		mainLight.intensity = 0.0f;
		pauseText.enabled = true;
		resumeButton.gameObject.SetActive (true);
		terminateButton.gameObject.SetActive (true);	
	}
}
