import org.newdawn.slick.Input;
import org.newdawn.slick.SlickException;

public class Engineer extends GameObject {
    public static final String SPRITE_PATH = "assets/units/engineer.png";
    public static final double ENGINEER_SPEED = 0.1;
    public static final int MINING_TIME = 5000;
    public static int capacity = 2;
    private GameObject nearCommandCentre;
    private GameObject mine = null;
    private double distance;
    private int pastTime = 0;
    private boolean mining = false;
    private double commandCentreDistance;
    private boolean miningUnobtanium = false;
    private boolean miningMetal = false;

    public Engineer(double x, double y) throws SlickException {
        setX(x);
        setY(y);
        setTargetY(y);
        setTargetX(x);
        setImage(SPRITE_PATH);
    }



    public void update(World world, Camera camera) {
        Input input = world.getInput();
        nearestCommandCentre(world);
        // If the mouse button is being clicked, set the target to the cursor location
        if (world.getSelected() == this) {
            if (input.isMousePressed(Input.MOUSE_RIGHT_BUTTON)) {
                pastTime = 0;
                mining = false;
                setTargetX(camera.screenXToGlobalX(input.getMouseX()));
                setTargetY(camera.screenYToGlobalY(input.getMouseY()));
            }
        }

        // If we're close to our target, reset to our current position
        if (World.distance(getX(), getY(), getTargetX(), getTargetY()) <= ENGINEER_SPEED) {
            resetTarget();

        } else {
            // Calculate the appropriate x and y distances
            double theta = Math.atan2(getTargetY() - getY(), getTargetX() - getX());
            double dx = (double) Math.cos(theta) * world.getDelta() * ENGINEER_SPEED;
            double dy = (double) Math.sin(theta) * world.getDelta() * ENGINEER_SPEED;
            // Check the tile is free before moving; otherwise, we stop moving
            if (world.isPositionFree(getX() + dx, getY() + dy)) {
                setX(super.getX() + dx);
                setY(super.getY() + dy);
            } else {
                pastTime = 0;
                mining = false;
                resetTarget();
            }
        }



  
        
        for (GameObject object: world.list) {
        	distance = World.distance(object.getX(), object.getY(), getX(), getY());
        	if(object instanceof CommandCentre) {
	            if ((miningMetal || miningUnobtanium) & distance < 10) {
	                goToMine();
	                if (miningMetal) {
	                    miningMetal = false;
	                    world.setMetal(capacity);
	                }
	                if (miningUnobtanium) {
	                	pastTime = 0 ;
	                    miningUnobtanium = false;
	                    world.setUnobtainiun(capacity);
	                }
	            }
        	}
            if (object instanceof MetalMine & distance < 10) {
            	mine(object, world);
            }

            if (object instanceof UnobtainiumMine & distance < 10) {
                mine(object, world);
            }

            if (pastTime > MINING_TIME & object instanceof MetalMine) {
                pastTime = 0;
                miningMetal = true;
                goToCommandCentre();
                }

            if (pastTime > MINING_TIME & object instanceof UnobtainiumMine) {
            	pastTime = 0 ;
                miningUnobtanium = true;
                goToCommandCentre();
            }
               
         }




        }



    
    
    
    
    
    
    

	public void nearestCommandCentre(World world) {
		for(GameObject object: world.list) {
            if (object instanceof CommandCentre) {
    			distance = World.distance(object.getX(), object.getY(), getX(), getY());
                if (nearCommandCentre == null) {
                    nearCommandCentre = object;
                    commandCentreDistance = World.distance(nearCommandCentre.getX(), nearCommandCentre.getY(), getX(), getY());
                }
                else if (!object.equals(nearCommandCentre) && distance < commandCentreDistance) {
                    nearCommandCentre = object;
                    commandCentreDistance = World.distance(nearCommandCentre.getX(), nearCommandCentre.getY(), getX(), getY());
                }
            }
		}	
	}
	
    
    public void mine(GameObject object, World world) {
    	if(!mining) {
    		mine = object;
    	}
    	mining  = true;
    	pastTime+= world.getDelta();
    }
    
	public void goToMine() {
		setTargetX(mine.getX());
		setTargetY(mine.getY());
	}
	
	public void goToCommandCentre() {
		setTargetX(nearCommandCentre.getX());
        setTargetY(nearCommandCentre.getY());
	}
	
	
	


}