##########################################################
#Author: Chetan Kumar ckumaronline@gmail.com
#Sample data pull scripts
#Prepare data for feature engineering / feature selection
#Create training and testing sets for Recommended Opportunities ML model
##########################################################


#sample SQL script for online ad campaign experiment
#data pull for creating a training dataset 
SELECT
   dq117_acc_int.sector,
   dq117_acc_int.sub_sector,
   dq117_acc_int.pod_name,
   dq117_acc_int.gt_product,
   dq117_acc_int.campaign_name,
   dq117_acc_int.advert_id,
   dq117_acc_int.division_name,
   dq117_acc_int.is_accepted2,
   dq117_acc_int.is_dismissed2,
   dq117_acc_int.is_pitched2,
   dq117_acc_int.is_won2,
   dq117_acc_int.is_activated2,
   dq117_acc_int.impact_surfaced,
   dq117_acc_int.impact_surfaced_current,
   dq117_acc_int.surface_type,
   dq117_acc_int.product_segment,
   dq117_acc_int.intent,
   dq416_acc_gt.accepted_gt_product_q416,
   dq117_acc_int.id2,
   approvals.offering_id AS approvals_id,
   revexp.offering_id AS revexp_id,
   #renaming column to present_impact_surfaced_start instead of should_surface_with_deal_value 
   CASE
      WHEN
         approvals.offering_id is null 
         AND revexp.offering_id is null 
      THEN
         0 
      ELSE
         1 
   END
   AS present_impact_surfaced_start, 
   CASE
      WHEN
         dq117_acc_int.impact_surfaced > 0 
      THEN
         1 
      ELSE
         0 
   END
   AS present_impact_surfaced, 
   CASE
      WHEN
         dq416_acc_gt.accepted_gt_product_q416 != 'NULL' 
      THEN
         1 
      ELSE
         0 
   END
   AS accepted_same_gt_product_previous_Q 
FROM
   (
      SELECT
         dq117.sector,
         dq117.sub_sector,
         dq117.pod_name,
         dq117.gt_product,
         dq117.campaign_name,
         dq117.advert_id,
         dq117.division_name,
         dq117.is_accepted2,
         dq117.is_dismissed2,
         dq117.is_pitched2,
         dq117.is_won2,
         dq117.is_activated2,
         dq117.impact_surfaced,
         dq117.impact_surfaced_current,
         dq117.id2,
         dq117.surface_type,
         dq117.product_segment,
         im117.intent AS intent 
      FROM
         datascape.ROpps_Datapack_Q117 dq117 
         #inner join for intent 
         INNER JOIN
            leadengine_dev.q117_ropps_menu im117 
            ON dq117.advert_id = im117.advert_id 
      WHERE
         (
            dq117.is_accepted2 = 1 
            OR dq117.is_dismissed2 = 1
         )
         AND is_surfaced = 1 
         AND dq117.country_code = 'US' 
         AND dq117.sector = 'Services & Distribution Solutions' 
      ORDER BY
         dq117.pod_name,
         dq117.gt_product,
         dq117.campaign_name
   )
   dq117_acc_int 
   #left join for accepted gt product previous Q 
   LEFT JOIN
      (
         SELECT DISTINCT
            gt_product AS accepted_gt_product_q416,
            pod_name 
         from
            datascape.ROpps_Datapack_Q416 
         WHERE
            (
               is_accepted2 = 1
            )
            AND is_surfaced = 1 
            AND country_code = 'US' 
            AND sector = 'Services & Distribution Solutions' 
         ORDER BY
            pod_name,
            accepted_gt_product_q416
      )
      dq416_acc_gt 
      ON dq117_acc_int.pod_name = dq416_acc_gt.pod_name 
      AND dq117_acc_int.gt_product = dq416_acc_gt.accepted_gt_product_q416 
   LEFT JOIN
      (
         SELECT
            offering_id 
         FROM
            datascape.leadengine_q117_approvals 
         WHERE
            approval_offering = 1 
            AND approval_revenue = 1
      )
      approvals 
      ON dq117_acc_int.advert_id = approvals.offering_id 
   LEFT JOIN
      (
         SELECT
            CAST(pod_id AS STRING) AS pod_id,
            offering_id 
         FROM
            datascape.rev_experiment_teams_q117
      )
      revexp 
      ON revexp.offering_id = dq117_acc_int.advert_id 
      AND revexp.pod_id = dq117_acc_int.id2;
 
 
#final lead_relevance_score generation
#for q317 test divisions/pods
#excluding selected offerings and custom lead lists
SELECT id2,
       id1,
       offering_id AS offering_id_q317,
       accepted_offering_id_q217,
       accepted_same_offering_id_previous_Q,
       product,
       accepted_gt_product_q217,
       accepted_same_gt_product_previous_Q,
       (accepted_same_offering_id_previous_Q + accepted_same_gt_product_previous_Q) AS lead_relevance_score
FROM
  ( SELECT q317.id2,
           q317.id1,
           q317.offering_id,
           q217_offering.accepted_offering_id_q217,
           CASE
               WHEN q217_offering.accepted_offering_id_q217 != 'NULL' THEN 1
               ELSE 0
           END AS accepted_same_offering_id_previous_Q,
           q317.product,
           q217_gt.accepted_gt_product_q217,
           CASE
               WHEN q217_gt.accepted_gt_product_q217 != 'NULL' THEN 1
               ELSE 0
           END AS accepted_same_gt_product_previous_Q
   FROM
     ( SELECT q317_qa.sales_advert_id AS offering_id,
              q317_qa.id1,
              CAST(q317_qa.id2 AS STRING) AS id2,
              q3_menu.product
      FROM datascape.leadengine_dremel.ropps_division_level_datapack_qa_q317 q317_qa
      INNER JOIN datascape.leadengine_dev.q317_ropps_menu q3_menu 
        ON q317_qa.sales_advert_id = q3_menu.advert_id
      INNER JOIN
        ( SELECT id1,
                 id2,
                 COUNT(*) AS total_offerings
         FROM datascape.leadengine_dremel.ropps_division_level_datapack_qa_q317 a
         INNER JOIN datascape.leadengine_dev.q317_ropps_menu b 
          ON a.sales_advert_id = b.advert_id
         WHERE LOWER(TRIM(b.segment)) != 'custom lead list'
           AND b.advert_id NOT IN ('B.0143.01',
                                     'B.0139.01',
                                     'X.0009.01',
                                     'X.0257.01',
                                     'P.0197.01',
                                     'P.0257.01',
                                     'P.0267.01')
         GROUP BY 1,
                  2 HAVING total_offerings >= 18) c 
        ON q317_qa.id1 = c.id1
      AND q317_qa.id2 = c.id2
      WHERE LOWER(TRIM(q3_menu.segment)) != 'custom lead list'
        AND q3_menu.advert_id NOT IN ('B.0143.01',
                                        'B.0139.01',
                                        'X.0009.01',
                                        'X.0257.01',
                                        'P.0197.01',
                                        'P.0257.01',
                                        'P.0267.01')) q317
   LEFT JOIN
     ( SELECT DISTINCT gt_product AS accepted_gt_product_q217,
                       id2,
                       id1
      FROM datascape.ROpps_Datapack_Q217
      WHERE (is_accepted2 = 1)) q217_gt 
    ON q317.product = q217_gt.accepted_gt_product_q217
   AND q317.id1 = q217_gt.id1
   AND q317.id2 = q217_gt.id2
   LEFT JOIN
     ( SELECT DISTINCT advert_id AS accepted_offering_id_q217,
                       campaign_name,
                       id2,
                       id1
      FROM datascape.ROpps_Datapack_Q217 d
      WHERE (is_accepted2 = 1)) q217_offering 
    ON q317.offering_id = q217_offering.accepted_offering_id_q217
   AND q317.id1 = q217_offering.id1
   AND q317.id2 = q217_offering.id2)
ORDER BY id2,
         id1,
         lead_relevance_score DESC;
         


#surfaced, reviewed, accepted, dismissed, review rate, and accept rate 
#for customer divisions in data_source_table 
#experiment test and control groups
SELECT id1,
       id2,
       test_control_group_flag,
       surfaced_count,
       accept_count,
       dismiss_count,
       (accept_count + dismiss_count) AS review_count,
       ((accept_count + dismiss_count) * 100 / surfaced_count) AS review_rate,
       CASE
           WHEN (accept_count + dismiss_count) != 0 THEN (accept_count * 100 / (accept_count + dismiss_count))
           ELSE 0
       END AS accept_rate
FROM       
(SELECT COUNT(DISTINCT d.advert_id) AS count_advert_id,
       SUM(is_accepted2) as accept_count, 
       SUM(is_dismissed2) as dismiss_count,
       SUM(is_surfaced) as surfaced_count,        
       d.id1, 
       CAST(d.id2 AS STRING) AS id2,
       r.class AS test_control_group_flag
FROM data_source_table d
INNER JOIN
  (SELECT id1, CAST(id2 AS STRING) AS id2, class
   FROM experiment_groups_test_control) r
 ON r.id1 = d.id1
AND CAST(r.id2 AS STRING) = d.id2
WHERE (d.is_surfaced = 1)
GROUP BY d.id1,
         d.id2,
         test_control_group_flag
ORDER BY test_control_group_flag DESC, 
         count_advert_id DESC);