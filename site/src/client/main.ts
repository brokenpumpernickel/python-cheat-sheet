// The client entry point: everything the page does after the build rendered it.
import { startArrangement } from "./arrangement";
import { startCopy } from "./copy";
import { startSearch } from "./search";
import { startTrail } from "./trail";
import { startViews } from "./views";

const views = startViews();
startArrangement(views.arrangementSwitched);
startTrail();
startCopy();
startSearch();
