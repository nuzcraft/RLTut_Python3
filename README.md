# RLTut_Python3

following the roguelike tutorial at http://rogueliketutorials.com/tutorials/tcod/v2/

Developing w/ Python 3.9.2 64-bit

I want to use this as an opportunity to:

1. relearn some python
2. relearn some tcod
3. implement unit tests
4. make a roguelike
5. practice with git

## Part 9 Dev Notes

### Ranged Scrolls and Targeting

https://rogueliketutorials.com/tutorials/tcod/v2/part-9/

Woot! No additional refactoring yet! This section should be fun because it will give us the opportunity to use the code we just built to add more items that do unique things. Hopefully (outside of targeting) the additional things should be relatively minor and relatively atomic.

This part was really insightful to develop as I believe it will pave the way for a significant amount of future development. We developed some unique spells that function in very different ways; one that automatically targets the nearest actor and 2 the require additional user input mid-cast. This additional input is implemented in an interesting way and by watching it get out in place I think I understand the code flow. 

From a unit testing standpoint, this part was intense. Adding new handlers for user input meant a significant amount of unit testing. I'm also noticing that there is a lot id dependencies around the player, engine, and game map objects that makes it cumbersome to set up tests on other objects. All in, unit testing is becoming more comfortable and I'm looking forward to a time when I feel like I can push what I know to make it more organized and more performant.

## Part 8 Dev Notes

### Items and Inventory

https://rogueliketutorials.com/tutorials/tcod/v2/part-8/

It looks like this is going to start off with a refactor(similar to part 6). Hopefully it doesn't result in quite as extensive of a unit test rewrite as the engine class rewrite.

Refactor complete. It wasn't nearly as broad as the engine refactor, and I like a lot of the ideas here. Make it clearer that certain things have parents to define that relationship (specifically to maps) but still allow entities to easily get the gamemap they're associated with. From a unit test perpsective, this broke ~25% of the tests, but they were easily fixed by swapping out 'gamemap' with 'parent' in almost all cases

This next section will begin soon! We'll be getting a working inventory set up as well as some items that can be picked up and used.

Okay, wow, well, that was a lot. This part in particular felt difficult because there were SO MANY backend pieces to put together before we see anything on the screen. That plus all the moving pieces meant that maintaining the unit tests was somewhat painful. In the end, I think the solutions here are quite flexible.

## Part 7 Dev Notes

### Creating the Interface

https://rogueliketutorials.com/tutorials/tcod/v2/part-7/

Heyo, it looks like this part will be focused on the UI. I'm looking forward to adding a bit of polish :). I'm also going to reorganize my Dev Notes so that the more recent dev notes show up on top.

Interestingly (or not I guess) I found it difficult to focus on part 7, and I think some of it was analysis paralysis on unit testing. I'm finding there are more and more things I want to unit test, but don't quite have the skills/experience to make it work; I don't understand what all unittest can do so my unit tests are pretty basic.

I think the above was compounded by UI work being a bit more cumbersome to unit test. This section did a lot of good work to make things look nice on the screen and in the end, I enjoyed making it happen.

Finally, merging the part 7 pull request was really nice :) the python unit testing code ran on its own, alerted me to a minor issue that kept me from merging until I fixed it. Very cool!

## Part 6.5 Building, Testing, Releasing, etc

I spent an evening futzing around with a couple things here that I want to document. Firstly, I set up a GitHub action that will very specifically build the project and run all my unit test whenever I commit to main! This is really nice as it will let me know if any code makes it to the repo that breaks some functions. This is a really important part of continuous integration even if I'm not really trying to continuously integrate this code anywhere. Secondly, I figured out how to use pyinstaller to build an executable of my python project. This has been difficult for me to do in the past, so it was really nice to get it somewhat figured out. The pyinstaller command I use to build is:

- pyinstaller --add-data "dejavu10x10_gs_tc.png;." main.py

This will build the python codebase and add the font file to the root of the folder. This goes into a 'dist' folder -> I can zip this up and distribute it as a release on GitHub!.

That's everything for this section I think. Any new unit tests I add should automatically be ran by the GitHub action. I may need to adjust my pyinstaller commands, especially as I add/alter external font files.

## Part 6 Dev Notes

### Doing (and taking) some damage

http://rogueliketutorials.com/tutorials/tcod/v2/part-6/

Heyo, it looks like this part is going to start with a bit of a code refactor! This means we'll be making lots of changes to our existing codebase + lots of changes to our existing unit tests. This part might be a bit of a pain...but we'll come through!

DONE:

1. rewrite input_handler unit tests once the Engine refactor is complete
2. rewrite our action unit tests once the engine refactor is complete
3. rewrite game_map unit tests once the engine refactor is complete
4. rewrite entity unit tests once the engine refactor is complete
5. rewrite procgen unit tests once the engine refactor is complete
6. rewrite engine unit tests not that the engine refactor is complete

😆 with this refactor, only 8 of my 44 unit tests are passing 😎 there's a lot of testing work to be done before we work on part 6 proper.

Alright! All done with the unit test refactor! I was right, there was a lot of work to do! When we change how objects are initialized, it causes problems all over the place.

I've started adding a few of the components (so far, BaseComponent, Fighter, and BaseAI) but I haven't implemented any of them yet. Writing unit tests for them has been helpful, I'm relatively confident their implementation will work without too many headaches, provided I use them as intended.

We're making progress. There have been a couple things I've had issues adding unit tests for - mostly in HostileEnemy.perform - we have a component that will call the perform function on a different class, which has proven difficult to mock. Otherwise, things are going smoothly.

And we're done!! I don't remember exactly how much time I spent on this part, I would hazard a week or so? The initial refactor and fixing of unit tests was pretty intense, then the subsequent code changes were pretty intense to! I've very happy with the results, and am reasonably confident in my learning progress so far. One thing I've got on my brain... this tutorial code IS NOT written to be robust, it's written to accept expected inputs and use them. As such, there is probably a lot of coding and testing that could be done to ensure that functions are only used as intended... that is extra work I'm not intending to do. I will implement positive and negative tests where applicable, but will likely not alter existing code to handle extra weird inputs at this time (nor look to test for them).

At the moment, I think the project is in a good spot where I can look to build up a deployment pipeline of some sort. I've never created releases for a python project, so this should be interesting.

## Part 5 Dev Notes

### Placing Enemies and kicking them (harmlessly)

http://rogueliketutorials.com/tutorials/tcod/v2/part-5/

Oh snap! Now that we have a dungeon, we're ready to start filling it with stuff! Let's get some monsters going!

This was a very fun chapter! We touched a lot of different functions, and I can see the pieces of things coming together really well. I liked the use of the BumpAction and I think it presented an interesting challenge for unit testing. As it stands, I'm starting to get confident in my ability to build and run the program and have it work as expected so long as my unit tests have passed! I think there's still plenty of room for improvement in them, but as it is, I'm happy with what I've learned.

## Part 4 Dev Notes

### Field of View

http://rogueliketutorials.com/tutorials/tcod/v2/part-4/

Field of view is a really cool...and really annoying part of roguelike development. I think I'm going to make sure I have an easy way to turn on and off FOV since it is way easier to debug issues with FOV off.

OOF, development is starting off rough. At some point in part 3 I removed pyvenv.cfg from the repo (since it directly relates to the local development environment) and it got deleted when I pulled again 😑 I'm not sure how to remove files from a repo without deleting them. It seems like .gitignore should apply to pulls as well, don't pull adds/deletes/changes to files in the .gitignore. Regardless, I think I got it back up and running.

Complete! I got most of the tests up and running well too! Except for engine.compute_fov - for some reason, I couldn't get it set up to assert the tcod.map.compute_fov was called or that the engine.game_map.visible array changed after calling it. Which is weird, because in gameplay it's working just fine. I will likely need to revisit if I find a bug in the code :)

## Part 3 Dev Notes

### Generating a Dungeon

http://rogueliketutorials.com/tutorials/tcod/v2/part-3/

I'm really looking forward to dungeon generation. The procedural nature is probably my favorite part of roguelike development/working through these tutorials.

This turned out to be quite a lot of fun. I liked breaking down the procgen into smaller pieces, rectangles and such. Unit testing is also going well? I'm not sure if I'm testing functions well, but it seems like some testing is better than none.

## Part 2 Dev Notes

### The generic Entity, the render functions, and the map

http://rogueliketutorials.com/tutorials/tcod/v2/part-2/

I had a good time setting up unit tests and such in part one, and I think part 2 is going to be a challenge. At this exact time, I'm looking at setting up unit tests for the engine scripts, am seeing functions that will be difficult to test, and am looking forward to the puzzle solving.

After quite a bit of futzing, I'm feeling really good about the development process here. Create script, write tests, implement code, see results. I think it will be really interesting to update/fix unit tests as the codebase changes. Part 2 is complete! Looking forward to part 3!

## Part 1 Dev Notes

### Drawing the '@' symbol and moving it around

http://rogueliketutorials.com/tutorials/tcod/v2/part-1/

It has been a long time since I did anything significant with python or tcod, so this should be a lot of fun.

Welp, after finishing part one, there is a lot of syntax in here that I'm not very familiar with. I think I understand the gist of what's happening, but it will take some work before I'm fully comfortable with it. Regardless, I'm really enjoying how this is going!

I got movin' and groovin' on unit testing and after some finagling I got a suite of unit tests running on the overwritten ev_quit and ev_keydown functions. I found this to be an educational experience, and look forward to setting up more unit tests as the codebase grows.
