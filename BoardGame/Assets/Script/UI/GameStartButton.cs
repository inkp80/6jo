using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameStartButton : MonoBehaviour {
	private string sceneName = "Game";

	public void PlayWithAI() {
		SceneManager.LoadScene (sceneName);
	}
}
