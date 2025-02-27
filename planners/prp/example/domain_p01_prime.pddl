(define (domain triangle-tire)
	(:requirements :typing :strips :non-deterministic)
	(:types location)
	(:predicates (vehicleat ?loc - location) (spare-in ?loc - location) (road ?from - location ?to - location) (not-flattire) (q1 ?loc-00 - location) (q2 ?loc-00 - location) (turnDomain))
	(:action move-car
		:parameters (?from - location ?to - location)
		:precondition (and (vehicleat ?from) (road ?from ?to) (not-flattire) (turnDomain))
		:effect (and (oneof (and (vehicleat ?to) (not (vehicleat ?from))) (and (vehicleat ?to) (not (vehicleat ?from)) (not (not-flattire)))) (not (turnDomain)))
	)
	(:action changetire
		:parameters (?loc - location)
		:precondition (and (spare-in ?loc) (vehicleat ?loc) (turnDomain))
		:effect (and (not (spare-in ?loc)) (not-flattire) (not (turnDomain)))
	)
	(:action trans-0
		:parameters (?loc-00 - location)
		:precondition (and (q1 ?loc-00) (not (vehicleat ?loc-00)) (not (turnDomain)))
		:effect (and (q1 ?loc-00) (not (q2 ?loc-00)) (turnDomain))
	)
	(:action trans-1
		:parameters (?loc-00 - location)
		:precondition (and (or (and (q1 ?loc-00) (vehicleat ?loc-00)) (q2 ?loc-00)) (not (turnDomain)))
		:effect (and (q2 ?loc-00) (not (q1 ?loc-00)) (turnDomain))
	)
)