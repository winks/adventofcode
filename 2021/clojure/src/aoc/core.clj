(ns aoc.core
  (:require [clojure.tools.cli :refer [parse-opts]])
  (:require [clojure.java.io :as io])
  (:gen-class))

(def cli-options
  [["-d" "--day DAY" "DAY"
    :default ""
    :validate [#(not (empty? %)) "Can't be empty"]]
  ["-f" "--file FILE" "FILE"
    :default ""]])

(defn runit [opt]
  (let [filename (if (empty? (:file opt)) (str "../input/day" (:day opt) "/input.txt") (:file opt))
        dayns (symbol (str "aoc.day" (:day opt)))]
    (when-let [src (.exists (io/file (str "src/aoc/day" (:day opt) ".clj")))]
      (require dayns)
      (let [fun (resolve (symbol (str "aoc.day" (:day opt) "/run")))]
        (println (str "\n### " dayns))
        (time (fun filename))))))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (let [opt (:options (parse-opts args cli-options))
        days (map (fn [x] (if (= 1 (count (str x))) (str "0" x) (str x))) (range 1 26))]
    (if (empty? (:day opt))
      (doall (map #(runit {:day %}) days))
      (runit opt))))
