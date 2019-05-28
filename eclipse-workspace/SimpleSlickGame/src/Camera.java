import org.newdawn.slick.Input;

/**
 * This class should be used to restrict the game's view to a subset of the entire world.
 * 
 * You are free to make ANY modifications you see fit.
 * These classes are provided simply as a starting point. You are not strictly required to use them.
 */
public class Camera {
	private double x = 300;
	private double y = 300;
	private GameObject target;
	private boolean locked;
	public static final double CAMERA_SPEED = 0.4 ; 
	
	public void followSprite(GameObject target) {
		this.target = target;
		locked = true;
	}
	
	public double globalXToScreenX(double x) {
		return x - this.x;
	}
	public double globalYToScreenY(double y) {
		return y - this.y;
	}

	public double screenXToGlobalX(double x) {
		return x + this.x;
	}
	public double screenYToGlobalY(double y) {
		return y + this.y;
	}
	
	public void update(World world) {
		Input input = world.getInput();
		if(locked){
			x = target.getX()- App.WINDOW_WIDTH/2;
			y = target.getY() - App.WINDOW_HEIGHT/2;	
		}
		
		if(input.isKeyDown(Input.KEY_W)) {
			locked = false;
			y -= CAMERA_SPEED * world.getDelta();
		}
		else if (input.isKeyDown(Input.KEY_A)) {
			locked = false;
			x -= CAMERA_SPEED * world.getDelta();
		}
		else if (input.isKeyDown(Input.KEY_S)) {
			locked = false;
			y +=  CAMERA_SPEED * world.getDelta();
		}
		else if (input.isKeyDown(Input.KEY_D)) {
			locked = false;
			x += CAMERA_SPEED * world.getDelta();
		}
		else { }
		
		x = Math.min(x, world.getMapWidth() - App.WINDOW_WIDTH);
		x = Math.max(x, 0);
		y = Math.min(y, world.getMapHeight() - App.WINDOW_HEIGHT);
		y = Math.max(y, 0);
	
	}
	
	
	

	public double getY() {
		return y;
	}

	public void setY(double y) {
		this.y = y;
	}

	public double getX() {
		return x;
	}

	public void setX(double x) {
		this.x = x;
	}
}
