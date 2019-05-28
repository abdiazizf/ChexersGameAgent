import org.newdawn.slick.Graphics;
import org.newdawn.slick.Image;
import org.newdawn.slick.SlickException;

public abstract class GameObject {
	public static final Image HIGHLIGHT;
	public static final Image LARGE_HIGHLIGHT;
	public static final int UNIT_BUILD_TIME  = 5000;
	private double x ;
	private double y ;
	private double targetX;
	private double targetY;
	private Image image ;
	static { 
		Image tmp = null;
		Image tmp1 = null;
		try {
			tmp = new Image("assets/highlight.png");
			tmp1 = new Image("assets/highlight_large.png");
		} catch (SlickException e) {
			
		}
		HIGHLIGHT = tmp;
		LARGE_HIGHLIGHT = tmp1;
		
	}
	

	
	public void render(Camera camera,World world, Graphics g) {
		if(this.equals(world.getSelected())) {
			
		HIGHLIGHT.drawCentered((float)camera.globalXToScreenX(x), 
		            (float)camera.globalYToScreenY(y));
		}
		
		
		image.drawCentered((float)camera.globalXToScreenX(x), 
			            (float)camera.globalYToScreenY(y));
		
		

	}

	public void resetTarget() {
		targetX = x;
		targetY = y;		
	}
	
	// GETTERS AND SETTERS
	public double getTargetY() {
		return targetY;
	}

	public void setTargetY(double targetY) {
		this.targetY = targetY;
	}

	public double getTargetX() {
		return targetX;
	}

	public void setTargetX(double targetX) {
		this.targetX = targetX;
	}
	
	public double getX() {
		return x;
	}
	
	public double getY() {
		return y ;
	}
	
	public void setX(double x) {
		this.x = x ;
	}
	
	public void setY(double y) {
		this.y = y ;
	}
	public Image getImage() {
		return image;
	}
	public void setImage(String path) throws SlickException {
		this.image = new Image(path);
	}

	public abstract void update( World world,Camera camera);

	

//WATCH OUT FOR SHADOW VARIABLE NAMES
}

