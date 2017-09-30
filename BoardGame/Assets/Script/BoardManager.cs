using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoardManager : MonoBehaviour {

	private const int WHITE_PLAYER = 0;
	private const int BLACK_PLAYER = -1;
	private const float TILE_SIZE = 1.0f;
	private const float TILE_OFFSET = 0.5f;

	//white player : 0 (play first) / black player : -1
	private int currentPlayer = 0; 
	private int selectionX = -1;
	private int selectionY = -1;

	private bool itemActiveState = false;
	private int itemCode = -1;


	public GameObject reversiPrefab;
	public Piece[,] activedPieces{ set; get; }

	private void Start(){
		activedPieces = new Piece[8, 8];
		initBoard ();
	}

	private void Update(){
		UpdateSelection ();
		DrawBoard ();

		if (Input.GetMouseButtonUp (0)) {
			
			startAction(selectionX, selectionY, currentPlayer);
		
		}
	}

	private void UpdateSelection(){
		if (!Camera.main) {
			return;
		}

		RaycastHit hit;
		if (Physics.Raycast (
			   Camera.main.ScreenPointToRay (Input.mousePosition), 
			   out hit, 
			   25.0f,
			   LayerMask.GetMask ("BoardPlane"))) {

			selectionX = (int)hit.point.x;
			selectionY = (int)hit.point.z;
//			Debug.Log (hit.point);
		} else {
			selectionX = -1;
			selectionY = -1;
		}
	}


	private void spawnPiece(int x, int y, int player){

		Vector3 spawnPosition = getTileCenter (x, y);
		Quaternion rotationState = 
			(player == WHITE_PLAYER) ? Quaternion.identity : Quaternion.AngleAxis (180, Vector3.left);

		GameObject go = Instantiate (reversiPrefab, spawnPosition, rotationState) as GameObject;
		go.transform.SetParent (transform);

		activedPieces [x, y] = go.GetComponent<Piece> ();
		activedPieces [x, y].setPosition (x, y);
		activedPieces [x, y].setColor (player);
	}

	private void initBoard(){
		spawnPiece (4, 3, WHITE_PLAYER);
		spawnPiece (4, 4, BLACK_PLAYER);

		spawnPiece (3, 3, BLACK_PLAYER);
		spawnPiece (3, 4, WHITE_PLAYER);
	}


	private void DrawBoard(){
		//single tile's size 1m * 8 * 8
		Vector3 widthLine = Vector3.right * 8;
		Vector3 heightLine = Vector3.forward * 8;


//		drawing checker box
		for (int i = 0; i <= 8; i++) {
			Vector3 start = Vector3.forward * i;
			Debug.DrawLine (start, start + widthLine);
			for (int j = 0; j <= 8; j++) {
				start = Vector3.right * i;
				Debug.DrawLine (start, start + heightLine);
			}
		}

		//Draw the selection
		if (selectionX >= 0 && selectionY >= 0) {
			Debug.DrawLine (
				Vector3.forward * selectionY + Vector3.right * selectionX,
				Vector3.forward * (selectionY + 1) + Vector3.right * (selectionX + 1)
			);

			Debug.DrawLine (
				Vector3.forward * (selectionY + 1) + Vector3.right * selectionX,
				Vector3.forward * selectionY + Vector3.right * (selectionX + 1)
			);
		}
	}


	private Vector3 getTileCenter(int x, int y){
		Vector3 origin = Vector3.zero;
		origin.x += (TILE_SIZE * x) + TILE_OFFSET;
		origin.z += (TILE_SIZE * y) + TILE_OFFSET;

		return origin;
	}
		
	private void startAction(int x, int y, int player){

		if (checkArrangeVaildation (x, y) == false) {
			return;
		}

		if (activedPieces [x, y] != null) {
			Debug.Log ("You can't select that area");
			activedPieces [x, y].flipPiece ();
			return;
		} else {
			Debug.Log ("current Player : " + currentPlayer);

			//TODO : Check is it possible area that can spawn piece.
			//if(checkSpawnAbility) ? true : false

		
			spawnPiece (x, y, currentPlayer);

			if (itemActiveState == true) {
				itemActiveState = false;
				Debug.Log ("Item code : " + itemCode); 
				switch (itemCode) {
				case 1: 
					Debug.Log ("filp activate");
					useFilpItem (x, y);
					break;
				case 2:
					useLineItem (x, y);
					break;
				default:
					break;
				}
			}

			currentPlayer = ~currentPlayer;
		}
	}

	public bool checkArrangeVaildation(int x, int y){
		if ((0 <= x && x < 8 ) && (0 <= y && y < 8)) {
			return true;
		} else {
			return false;
		}
	}


	public void activateItem(int itemCode){
		Debug.Log ("Item Seleceted");
		this.itemCode = itemCode;
		itemActiveState = true;
	}

	private void useFilpItem(int x, int y){
		for (int i = 0; i < 8; i++) {
			int nextX = dx [i] + x;
			int nextY = dy [i] + y;

			if (checkArrangeVaildation (nextX, nextY)) {
				if (activedPieces [nextX, nextY] != null) {
					activedPieces [nextX, nextY].flipPiece ();
					activedPieces [nextX, nextY].setColor (currentPlayer);
				}
			}
		}
	}

	int[] dx = { 0, 1, 1, 1, 0, -1, -1, -1 };
	int[] dy = { 1, 1, 0, -1, -1, -1, 0, 1 };


	private void useLineItem(int x, int y){
		for (int i = 0; i < 8; i++) {
			if (i == x) {
				continue;
			} else {
				if (activedPieces [i, y] != null
					&& currentPlayer != activedPieces [i, y].getColor ()) {
					activedPieces [i, y].flipPiece ();
					activedPieces [i, y].setColor (currentPlayer);
				}
			}
		}
		for (int i = 0; i < 8; i++) {
			if (i == y) {
				continue;
			} else {
				if (activedPieces [x, i] != null
					&& currentPlayer != activedPieces [x, i].getColor ()) {
					activedPieces [x, i].flipPiece ();
					activedPieces [x, i].setColor (currentPlayer);
				}
			}
		}


	}

}
