(ns day06.core
  (:require [clojure.tools.cli :refer [parse-opts]])
  (:require [clojure.string :as str])
  (:gen-class))

(def cli-options
  [["-i" "--input FILE" "FILE"
    :default ""
    :validate [#(not (empty? %)) "Can't be empty"]]])

(defn f-lines [file]
  (str/split-lines (slurp file)))

(defn tuples [v]
  (map #(conj [] (keyword (first %)) (keyword (second %)))
    (map #(str/split % #"\)") v)))

(defn app [s m]
  (let [p (str/split s #"\)")
        lx (keyword (first p))
        rx (keyword (second p))]
       (into m [[rx lx]])))

(defn organize [lst]
    (reduce into (map #(app % {}) lst)))

(defn isleaf? [k rd]
  (> 1 (count (filter #(= (second %) k) rd))))

(defn walk [outer all acc]
  (if (not (some #(= outer (first %)) all))
    []
    (if (= :COM outer)
      (cons outer acc)
      (let [s (get-in all [outer])]
        (cons outer (walk s all acc))))))

(defn counter3 [path acc done]
  (if (empty? path)
    [acc done]
    (if (some #(= (last path) %) done)
      (counter3 (butlast path) acc                         done)
      (counter3 (butlast path) (+ acc (dec (count path))) (conj done (last path))))))

(defn counter2 [paths acc done]
  (if (empty? paths)
    acc
    (let [[acc2 done2] (counter3 (first paths) 0 done)]
      (counter2 (rest paths) (+ acc acc2) done2))))

(defn part2 [a b r]
  (if (= (last a) (last b))
    (part2 (butlast a) (butlast b) r)
    (- (+ (count a) (count b)) 2)))

(defn -main [& args]
  (time
  (let [opt (:options (parse-opts args cli-options))
        lines (f-lines (:input opt))
        data (tuples lines)
        revdata (organize lines)
        leaves (map second (filter #(isleaf? (second %) revdata) data))
        paths (map reverse (map #(walk % revdata []) leaves))]
    (println "Part 1: Orbits: " (counter2 paths 0 []))
  (let [xy (walk :YOU revdata [])
        xs (walk :SAN revdata [])]
    (println "Part 2: Hops  : " (part2 xs xy 0))
    (println "")))))

(comment this would probably be nicer than counter2+counter3
(let [xx '((A B C D) (A B C E) (A X Y))
      indexed (mapcat #(zipmap % (range)) xx)]
  (reduce (fn [{:keys [seen sum] :as acc} [k i]]
            (if (contains? seen k)
              acc
              (-> acc
                  (update :seen conj k)
                  (update :sum + i))))
          {:seen #{} :sum 0}
          indexed))
; ⇒ {:seen #{A B C D E X Y}, :sum 12}

(defn countermeh [leaves revdata]
  (reduce + (map #(dec (count %)) (map #(walk (last %) revdata []) leaves))))
)
