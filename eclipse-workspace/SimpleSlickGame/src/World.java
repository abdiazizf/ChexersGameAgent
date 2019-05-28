import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

import org.newdawn.slick.Graphics;
import org.newdawn.slick.Input;
import org.newdawn.slick.SlickException;
import org.newdawn.slick.tiled.TiledMap;

/**
 * This class should be used to contain all the different objects in your game world, and schedule their interactions.
 * 
 * You are free to make ANY modifications you see fit.
 * These classes are provided simply as a starting point. You are not strictly required to use them.
 */
public class World {
	private static final String MAP_PATH = "assets/main.tmx";
	private static final String SOLID_PROPERTY = "solid";
	private static final String OCCUPIED_PROPERTY = "occupied";
	private static final String COMMA_DELIMITER = ",";
	public ArrayList<GameObject> list = new ArrayList<>();
	public ArrayList<GameObject> addlist = new ArrayList<>();
	public ArrayList<GameObject> removelist = new ArrayList<>();
	public ArrayList<GameObject> moving = new ArrayList<>();
	private int metal;
	private int unobtanium;
	private TiledMap map;
	private Camera camera = new Camera();
	private GameObject selected = null ; 
	private Input lastInput;
	private int lastDelta;
	private double mouseX;
	private double mouseY;
	private boolean click = false;


	
	
	public World() throws SlickException, FileNotFoundException, IOException {
		map = new TiledMap(MAP_PATH);
		try (BufferedReader br = new BufferedReader(new FileReader("assets/objects.csv"))) {
		    String line;
		    while ((line = br.readLine()) != null) {
		        String[] values = line.split(COMMA_DELIMITER);
		        double x = Double.valueOf(values[1]);
	        	double y = Double.valueOf(values[2]);
		        if(values[0].equals("command_centre")) {
		        	GameObject command_centre = new CommandCentre(x,y) ;
		        	list.add(command_centre);
		        }
		        else if (values[0].equals("metal_mine")) {
		        	GameObject mine = new MetalMine(x, y) ;
		        	list.add(mine);
		        }
		        
		        else if (values[0].equals("unobtainium_mine")) {
		        	GameObject mine = new UnobtainiumMine(x, y);
		        	list.add(mine);
		        }
		        
		        else if (values[0].equals("pylon")) {
		        	GameObject pylon = new Pylon(x, y);
		        	list.add(pylon);
		        }
		        
		        else { 
		        	GameObject engineer = new Engineer(x,y);
		        	list.add(engineer);
		        	
		        }
		    }
		}
	}
	
	
	public void update(Input input, int delta) {
		lastInput = input;
		lastDelta = delta;
		camera.update(this);
		
		if(input.isMousePressed(Input.MOUSE_LEFT_BUTTON)) {
			click = true;
			mouseX = camera.screenXToGlobalX(input.getMouseX());
			mouseY = camera.screenYToGlobalY(input.getMouseY());
		}
		
		for(GameObject object : list) {
			double near = distance(mouseX,mouseY,object.getX(),object.getY());
			if(near < 32 & selected == null) {
				click = false;
				selected = object;
				camera.followSprite(selected);
			}
			
			if(click) {
				selected = null;
			}
			
			
			object.update(this, camera);

		}
		
		for(GameObject object : addlist) {
			list.add(object);
		}
		addlist.clear();
		
		for(GameObject object : removelist) {
			list.remove(object);
		}
		removelist.clear();
	}


	public void render(Graphics g) {
		map.render((int)camera.globalXToScreenX(0),
				   (int)camera.globalYToScreenY(0));
		for(GameObject object : list) {
			object.render(camera, this , g);
		}
		
		
		if(selected instanceof CommandCentre) {
			g.drawString("1. Create Scout\n2- Create Builder\n3- Create Engineer",32,100);
		}
		else if(selected instanceof Factory) {
			g.drawString("1. Create Truck", 32, 100);
		}
		else if(selected instanceof Truck) {
			g.drawString("1. Create Command Centre", 32, 100);
		}
		g.drawString("Metal: "+ Integer.toString(metal) +"\nUnobtainium : " + Integer.toString(unobtanium), 32, 32 );
	
	}
	
	// This should probably be in a separate static utilities class, but it's a bit excessive for one method.
	public static double distance(double x1, double y1, double x2, double y2) {
		return (double)Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
	}
	
	public boolean isPositionFree(double x, double y) {
		int tileId = map.getTileId(worldXToTileX(x), worldYToTileY(y), 0);
		return !Boolean.parseBoolean(map.getTileProperty(tileId, SOLID_PROPERTY, "false"));
	}
	
	public boolean isBuildable(double x, double y) {
		int tileId = map.getTileId(worldXToTileX(x), worldYToTileY(y), 0 );
		return !Boolean.parseBoolean(map.getTileProperty(tileId,OCCUPIED_PROPERTY, "false"));
	}
	
	
	private int worldXToTileX(double x) {
		return (int)(x / map.getTileWidth());
	}
	
	private int worldYToTileY(double y) {
		return (int)(y / map.getTileHeight());
	}
	
	public Input getInput() {
		return lastInput;
	}
	
	public int getDelta() {
		return lastDelta;
	}
	
	public double getMapWidth() {
		return map.getWidth() * map.getTileWidth();
	}
	
	public double getMapHeight() {
		return map.getHeight() * map.getTileHeight();
	}


	public GameObject getSelected() {
		return selected;
	}


	public void setSelected(GameObject selected) {
		this.selected = selected;
	}
	
	public int getMetal() {
		return metal;
	}
	
	public void setMetal(int amount) {
		this.metal += amount;
	}
	public int getUnobtainium() {
		return unobtanium;
	}
	
	public void setUnobtainiun(int amount) {
		this.unobtanium += amount;
	}


	public ArrayList<GameObject> getAddlist() {
		return addlist;
	}


	public void setAddlist(ArrayList<GameObject> addlist) {
		this.addlist = addlist;
	}


	public ArrayList<GameObject> getRemovelist() {
		return removelist;
	}


	public void setRemovelist(ArrayList<GameObject> removelist) {
		this.removelist = removelist;
	}
}
