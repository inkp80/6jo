using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SplashScript : MonoBehaviour {

	private float delayTime = 3;
	// Use this for initialization
	void Start () {
		Invoke ("invokeThis", 3);
	}

	public void invokeThis(){
		StartCoroutine(startLoad("MainUI"));
	}
		

	public IEnumerator startLoad(string sceneName){
		AsyncOperation asyncOperation 
			= Application.LoadLevelAsync (sceneName);
		yield return true;
	}
}
