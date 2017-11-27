using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class MenuButton : MonoBehaviour {
	public Light mainLight;
	public Text pauseText;

	public void MenuOpen() {
		BoardManager.nextFire = Time.time + 1.0f;

		if (BoardManager.pauseFlag) {
			BoardManager.pauseFlag = false;
			mainLight.intensity = 1.0f;
			pauseText.enabled = false;
		} else {
			BoardManager.pauseFlag = true;
			mainLight.intensity = 0.0f;
			pauseText.enabled = true;
		}
	}
}
