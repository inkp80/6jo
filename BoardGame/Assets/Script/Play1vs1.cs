using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Play1vs1 : MonoBehaviour {
	private string sceneName = "Game";

	public void PlayWithHuman() {
		SceneManager.LoadScene (sceneName);
	}
}
