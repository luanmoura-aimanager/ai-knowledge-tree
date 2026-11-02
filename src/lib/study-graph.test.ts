import assert from "node:assert/strict";
import { test } from "node:test";
import { getCurriculum, lessonKey, studyMap } from "@/lib/curriculum";
import type { ProgressMap } from "@/lib/progress";
import {
  MAX_ZOOM,
  studyFraction,
  studyOpacity,
  zoomLimitAt,
} from "@/lib/study-graph";

test("zoomLimitAt treats float drift after zooming back out as full view", () => {
  const step = 1.6;
  let k = 1;
  for (const factor of [step, step, 1 / step, 1 / step]) k *= factor;
  assert.notEqual(k, 1);
  assert.equal(zoomLimitAt(k), "min");
});

test("zoomLimitAt reports the ends and the range between them", () => {
  assert.equal(zoomLimitAt(1), "min");
  assert.equal(zoomLimitAt(1.6), null);
  assert.equal(zoomLimitAt(MAX_ZOOM), "max");
});

test("studyFraction counts an in-progress lesson for half", () => {
  assert.equal(
    studyFraction({
      total: 4,
      studied: 1,
      inProgress: 2,
      state: "in-progress",
    }),
    0.5,
  );
});

test("studyFraction is 0 for missing or empty subsections", () => {
  assert.equal(studyFraction(undefined), 0);
  assert.equal(
    studyFraction({ total: 0, studied: 0, inProgress: 0, state: "untouched" }),
    0,
  );
});

test("studyOpacity keeps the dim look at 0 and a visible floor once started", () => {
  assert.equal(studyOpacity(0), "var(--dim-opacity)");
  assert.ok(Number(studyOpacity(1 / 34)) > 0.38);
  assert.equal(Number(studyOpacity(1)), 1);
});

test("studyMap rolls lesson progress up to every subsection", () => {
  const progress: ProgressMap = new Map(
    getCurriculum("A1").map((l) => [lessonKey("A1", l.id), "studied"]),
  );
  const [first] = getCurriculum("A2");
  progress.set(lessonKey("A2", first.id), "in-progress");

  const study = studyMap(progress);
  assert.equal(study.A1.state, "done");
  assert.equal(study.A1.studied, study.A1.total);
  assert.equal(study.A2.state, "in-progress");
  assert.equal(study.A2.inProgress, 1);
  assert.equal(study.B1.state, "untouched");
});
