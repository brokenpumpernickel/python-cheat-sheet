// The client entry point: everything the page does after the build rendered it.
import { startCopy } from "./copy";
import { startSearch } from "./search";
import { startViews } from "./views";

startViews();
startCopy();
startSearch();
