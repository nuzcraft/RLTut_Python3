# RLTut_Python3

following the roguelike tutorial at http://rogueliketutorials.com/tutorials/tcod/v2/

Developing w/ Python 3.9.2 64-bit

I want to use this as an opportunity to:

1. relearn some python
2. relearn some tcod
3. implement unit tests
4. make a roguelike
5. practice with git

## Part 1 Dev Notes

### Drawing the '@' symbol and moving it around

http://rogueliketutorials.com/tutorials/tcod/v2/part-1/

It has been a long time since I did anything significant with python or tcod, so this should be a lot of fun.

Welp, after finishing part one, there is a lot of syntax in here that I'm not very familiar with. I think I understand the gist of what's happening, but it will take some work before I'm fully comfortable with it. Regardless, I'm really enjoying how this is going!

I got movin' and groovin' on unit testing and after some finagling I got a suite of unit tests running on the overwritten ev_quit and ev_keydown functions. I found this to be an educational experience, and look forward to setting up more unit tests as the codebase grows.

## Part 2 Dev Notes

### The generic Entity, the render functions, and the map

http://rogueliketutorials.com/tutorials/tcod/v2/part-2/

I had a good time setting up unit tests and such in part one, and I think part 2 is going to be a challenge. At this exact time, I'm looking at setting up unit tests for the engine scripts, am seeing functions that will be difficult to test, and am looking forward to the puzzle solving.

After quite a bit of futzing, I'm feeling really good about the development process here. Create script, write tests, implement code, see results. I think it will be really interesting to update/fix unit tests as the codebase changes. Part 2 is complete! Looking forward to part 3!

## Part 3 Dev Notes

### Generating a Dungeon

http://rogueliketutorials.com/tutorials/tcod/v2/part-3/

I'm really looking forward to dungeon generation. The procedural nature is probably my favorite part of roguelike development/working through these tutorials.

This turned out to be quite a lot of fun. I liked breaking down the procgen into smaller pieces, rectangles and such. Unit testing is also going well? I'm not sure if I'm testing functions well, but it seems like some testing is better than none.

## Part 4 Dev Notes

### Field of View

http://rogueliketutorials.com/tutorials/tcod/v2/part-4/

Field of view is a really cool...and really annoying part of roguelike development. I think I'm going to make sure I have an easy way to turn on and off FOV since it is way easier to debug issues with FOV off.

OOF, development is starting off rough. At some point in part 3 I removed pyvenv.cfg from the repo (since it directly relates to the local development environment) and it got deleted when I pulled again 😑 I'm not sure how to remove files from a repo without deleting them. It seems like .gitignore should apply to pulls as well, don't pull adds/deletes/changes to files in the .gitignore. Regardless, I think I got it back up and running.

Complete! I got most of the tests up and running well too! Except for engine.compute_fov - for some reason, I couldn't get it set up to assert the tcod.map.compute_fov was called or that the engine.game_map.visible array changed after calling it. Which is weird, because in gameplay it's working just fine. I will likely need to revisit if I find a bug in the code :)

## Part 5 Dev Notes

### Placing Enemies and kicking them (harmlessly)

http://rogueliketutorials.com/tutorials/tcod/v2/part-5/

Oh snap! Now that we have a dungeon, we're ready to start filling it with stuff! Let's get some monsters going!

This was a very fun chapter! We touched a lot of different functions, and I can see the pieces of things coming together really well. I liked the use of the BumpAction and I think it presented an interesting challenge for unit testing. As it stands, I'm starting to get confident in my ability to build and run the program and have it work as expected so long as my unit tests have passed! I think there's still plenty of room for improvement in them, but as it is, I'm happy with what I've learned.

## Part 6 Dev Notes

### Doing (and taking) some damage

http://rogueliketutorials.com/tutorials/tcod/v2/part-6/

Heyo, it looks like this part is going to start with a bit of a code refactor! This means we'll be making lots of changes to our existing codebase + lots of changes to our existing unit tests. This part might be a bit of a pain...but we'll come through!

TODO:

1. rewrite input_handler unit tests once the Engine refactor is complete
2. rewrite our action unit tests once the engine refactor is complete
3. rewrite game_map unit tests once the engine refactor is complete
4. rewrite entity unit tests once the engine refactor is complete
5. rewrite procgen unit tests once the engine refactor is complete
6. rewrite engine unit tests not that the engine refactor is complete
