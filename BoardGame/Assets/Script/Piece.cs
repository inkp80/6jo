using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Piece : MonoBehaviour {
	
	private const int WHITE_PIECE = 0;	
	private const int BLACK_PIECE = -1;

	private Rigidbody rigidbody;
	private int pieceColor;
	private int positionX = -1;
	private int positionY = -1;

	public void Start(){
		rigidbody = GetComponent<Rigidbody> ();
	}
		
	public void reversePiece(){
		this.pieceColor = ~pieceColor;
	}

	public void setPosition(int x, int y){
		this.positionX = x;
		this.positionY = y;
	}

	public int getPositionX(){
		return positionX;
	}

	public int getPositionY(){
		return positionY;
	}

	public void setColor(int playerColor){
		pieceColor = playerColor;
	}

	public int getColor(){
		return pieceColor;
	}


	public void flipPiece(){
//		rigidbody.MoveRotation (Quaternion.AngleAxis (180, Vector3.left));
		rigidbody.AddForce (Vector3.up * 345);
		rigidbody.AddTorque (0, 0, 5);
	}


//	public IEnumerator flipPiece()
//	{
//		rigidbody.useGravity = false;
//		while (rigidbody.position.y < 2)
//		{
//			rigidbody.AddForce (Vector3.up * 50 * (2 - rigidbody.position.y));
//			//rigidbody.AddForce (Vector3.up * 560);
//			yield return new WaitForSeconds(.05f);
//		}
//		yield return new WaitForSeconds(.15f);
//
//		//rigidbody.AddForce (Vector3.up * 100);
//		rigidbody.AddTorque (0, 0, 8);
//		rigidbody.useGravity = true;
//	}


//	private bool isTriggered = false;
//	private void OnTriggerEnter(Collider other){
//		if (isTriggered == false) {
//			if (other.gameObject.CompareTag ("GameBoard")) {
//
//				Vector3 origin = Vector3.zero;
//				origin.x += (1.0f * positionX) + 0.5f;
//				origin.z += (1.0f * positionY) + 0.5f;
//				origin.y += 10.0f;
//				rigidbody.MovePosition (origin);
//
//				Debug.Log ("trigger enter : " + positionX + ", " + positionY);
//				rigidbody.MovePosition (origin);
//			}
//			isTriggered = true;
//		}
//	}
		
		
}
