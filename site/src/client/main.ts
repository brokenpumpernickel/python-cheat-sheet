// The client entry point: everything the page does after the build rendered it.
import { startArrangement } from "./arrangement";
import { startCopy } from "./copy";
import { startLanguage } from "./language";
import { startSearch } from "./search";
import { startTrail } from "./trail";
import { startViews } from "./views";

const views = startViews();
const search = startSearch();
startArrangement(views.arrangementSwitched);
startLanguage((change) => {
  views.keepPlace(change);
  search.languageSwitched();
});
startTrail();
startCopy();
