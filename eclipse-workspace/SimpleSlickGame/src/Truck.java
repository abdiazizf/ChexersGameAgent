import org.newdawn.slick.Input;
import org.newdawn.slick.SlickException;

public class Truck extends GameObject {
	public static final String TRUCK_PATH = "assets/units/truck.png" ;
	public static final double TRUCK_SPEED = 0.25;
	public static final int COMMAND_CENTRE_BUILD_TIME  = 15000;
	private boolean isBuildingCommandCentre = false;
	private int pastTime;
	
	public Truck(double x , double y) throws SlickException {
		 setX(x);
		 setY(y);
		 setTargetY(y);
		 setTargetX(x);
		 setImage(TRUCK_PATH);
	}
	
	public void update(World world, Camera camera) {
		Input input = world.getInput();
		
		// If the mouse button is being clicked, set the target to the cursor location
		if(world.getSelected() == this) {	
		if (input.isMousePressed(Input.MOUSE_RIGHT_BUTTON)) {
			setTargetX(camera.screenXToGlobalX(input.getMouseX()));
			setTargetY(camera.screenYToGlobalY(input.getMouseY()));
		}
		
		if(input.isKeyPressed(input.KEY_1) & !isBuildingCommandCentre)
		{
			if(world.isBuildable(getX() + 10 , getX()+ 10));
			isBuildingCommandCentre = true;
		}
		
		
		}
		// If we're close to our target, reset to our current position
		if (World.distance(getX(), getY(), getTargetX(), getTargetY()) <= TRUCK_SPEED) {
			resetTarget();
		} else {
			// Calculate the appropriate x and y distances
			double theta = Math.atan2(getTargetY() - getY(), getTargetX() - getX());
			double dx = (double)Math.cos(theta) * world.getDelta() * TRUCK_SPEED;
			double dy = (double)Math.sin(theta) * world.getDelta() * TRUCK_SPEED;
			// Check the tile is free before moving; otherwise, we stop moving
			if (world.isPositionFree(getX() + dx, getY() + dy)) {
				setX(getX() + dx);
				setY(getY() + dy);
			} else {
				resetTarget();
			}
		}
		
		
		if(isBuildingCommandCentre) {
			buildTruck(world);
		}
	}
	
	public void buildTruck(World world) {
		if(pastTime > COMMAND_CENTRE_BUILD_TIME) {
			try {
				isBuildingCommandCentre= false;
				pastTime= 0 ;
				GameObject newCommandCentre = new CommandCentre(this.getX()+10, this.getY() + 10);
				world.addlist.add(newCommandCentre);
			} catch (SlickException e) {
				e.printStackTrace();
			}
		}
		else {
			pastTime += world.getDelta();
		}
		
	}
	
}
