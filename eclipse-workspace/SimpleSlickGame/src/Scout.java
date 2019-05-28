import org.newdawn.slick.Input;
import org.newdawn.slick.SlickException;

public class Scout extends GameObject {
	public static final String SCOUT_PATH = "assets/units/scout.png";
	public static final double SCOUT_SPEED = 0.3;
	
	public Scout(double x, double y) throws SlickException {
		setX(x);
		setY(y);
		setTargetY(y);
		setTargetX(x);
		setImage(SCOUT_PATH);
	}
	
	public void update(World world, Camera camera) {
		Input input = world.getInput();
		
		// If the mouse button is being clicked, set the target to the cursor location
		if(world.getSelected() == this) {
		if (input.isMousePressed(Input.MOUSE_RIGHT_BUTTON)) {
			setTargetX(camera.screenXToGlobalX(input.getMouseX()));
			setTargetY(camera.screenYToGlobalY(input.getMouseY()));
			}
		}
		
		// If we're close to our target, reset to our current position
		if (World.distance(getX(), getY(), getTargetX(), getTargetY()) <= SCOUT_SPEED) {
			resetTarget();
		} else {
			// Calculate the appropriate x and y distances
			double theta = Math.atan2(getTargetY() - getY(), getTargetX() - getX());
			double dx = (double)Math.cos(theta) * world.getDelta() * SCOUT_SPEED;
			double dy = (double)Math.sin(theta) * world.getDelta() * SCOUT_SPEED;
			// Check the tile is free before moving; otherwise, we stop moving
			if (world.isPositionFree(getX() + dx, getY() + dy)) {
				setX(getX() + dx);
				setY(getY() + dy);
			} else {
				super.resetTarget();
			}
		}
	}


}
